import os
import torch
from apphelper.image import xy_rotate_box, box_rotate, solve
from apphelper.image_comac import plot_boxes
from apphelper.xml_read import GetAnnotBoxLoc
import model
import cv2
import numpy as np
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PIL import Image
from pandas import DataFrame
GPUID = '0'  # 调用GPU序号
os.environ["CUDA_VISIBLE_DEVICES"] = GPUID


def _OCR(img):
    _, result, angle = model.model(img,
                                   detectAngle=False,  # 是否进行文字方向检测
                                   config=dict(MAX_HORIZONTAL_GAP=36,
                                               # 字符之间的最大间隔，用于文本行的合并
                                               MIN_V_OVERLAPS=0.6,
                                               MIN_SIZE_SIM=0.6,
                                               TEXT_PROPOSALS_MIN_SCORE=0.1,
                                               TEXT_PROPOSALS_NMS_THRESH=0.3,
                                               TEXT_LINE_NMS_THRESH=0.7,
                                               # 文本行之间测iou值
                                               ),
                                   leftAdjust=True,  # 对检测的文本行进行向左延伸
                                   rightAdjust=True,  # 对检测的文本行进行向右延伸
                                   alph=0.01,  # 对检测的文本行进行向右、左延伸的倍数
                                   )
    return result, angle


p = './test/11.jpg'
img = cv2.imread(p)

h, w = img.shape[:2]
result, _ = _OCR(img)
boundboxes = GetAnnotBoxLoc("./label/附件修理翻修报告.xml")

# 获取对应基准点坐标对，计算最优仿射变换矩阵
points_from = []
points_to = []
result_dict = {line['text']: [line['cx'], line['cy'],
                              line['w'], line['h']] for line in result}
for k, v in boundboxes.items():
    if k[:3] != 'key':
        continue
    a = process.extractOne(k[3:], result_dict.keys(),
                           scorer=fuzz.ratio, score_cutoff=90)
    if a:
        points_from.append([result_dict[a[0]][0], result_dict[a[0]][1]])
        points_to.append([v[0], v[1]])
        # print(points_from)
        # print(points_to)
affine_transform_matrix = cv2.estimateAffine2D(
    np.array(points_from), np.array(points_to))
# print(affine_transform_matrix[0])
dstImg = cv2.warpAffine(img, affine_transform_matrix[0], (
    w, h), borderMode=cv2.INTER_LINEAR, borderValue=cv2.BORDER_REPLICATE)


result, angle = _OCR(dstImg)
plot_boxes(dstImg, angle, result, color=(0, 0, 0))
with open('test/output.txt', 'w') as f:
    for line in result:
        f.write(line['text']+'\n')

result_dict = {line['text']: [line['cx'], line['cy'],
                              line['w'], line['h']] for line in result}
structure_data = {}
csv_data = DataFrame()
for key, value in boundboxes.items():
    if key[:3] is 'key':
        continue
    structure_data[key] = ''
    for k, v in result_dict.items():
        if (v[0]-v[2]/2 > value[0]-value[2]/2 and
            v[0]+v[2]/2 < value[0]+value[2]/2 and
            v[1]-v[3]/2 > value[1]-value[3]/2 and
                v[1]+v[3]/2 < value[1]+value[3]/2):
            if '口' in k or k is '冈':
                continue
            structure_data[key] += k
csv_data = csv_data.append(structure_data, ignore_index=True)
# csv_data.to_csv('test/1.csv',sep=';',encoding='utf-8')  # windows下会乱码
csv_data.to_csv('test/1.csv', encoding='utf_8_sig')
