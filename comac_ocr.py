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
GPUID = '0'  # 调用GPU序号
os.environ["CUDA_VISIBLE_DEVICES"] = GPUID


p = './test/1.jpg'
img = cv2.imread(p)

h, w = img.shape[:2]
_, result, angle = model.model(img,
                                    detectAngle=True,  # 是否进行文字方向检测
                                    config=dict(MAX_HORIZONTAL_GAP=50,  # 字符之间的最大间隔，用于文本行的合并
                                    MIN_V_OVERLAPS=0.6,
                                    MIN_SIZE_SIM=0.6,
                                    TEXT_PROPOSALS_MIN_SCORE=0.1,
                                    TEXT_PROPOSALS_NMS_THRESH=0.3,
                                    TEXT_LINE_NMS_THRESH=0.7,  # 文本行之间测iou值
                ),
                                    leftAdjust=True,  # 对检测的文本行进行向左延伸
                                    rightAdjust=True,  # 对检测的文本行进行向右延伸
                                    alph=0.01,  # 对检测的文本行进行向右、左延伸的倍数
                                   )

boundboxes = GetAnnotBoxLoc("./label/附件修理翻修报告.xml")


for k, v in boundboxes.items():
    process.extract(k, result)

    

res_out = open('test/output.txt', 'w')
for line in result:
    print(line['text'])
    for k, v in line.items():
        res_out.write(str(k))
        res_out.write(' ')
        res_out.write(str(v))
        res_out.write(' ')
    res_out.write('\n')
res_out.close()
plot_boxes(img, angle, result, color=(0, 0, 0))