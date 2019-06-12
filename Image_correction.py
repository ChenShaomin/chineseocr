import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

p = "./test/11.jpg"
oriImg = cv2.imread(p)

oriPoints = np.float32([[896.75,145.0],[1246.5,336.0], [796.0,407.25]])
canvasPoints = np.float32([[797.25,143.5],[1151.25,297.5],[710.75,415.25]])

rotationMatrix = cv2.getAffineTransform(np.array(oriPoints),np.array(canvasPoints))

dstImg = cv2.warpAffine(oriImg,rotationMatrix,(1664,2352))
# cv2.imshow("perspectiveImg", dstImg)
plt.imsave("./test/11out.jpg", dstImg)
plt.figure('image')
plt.imshow(dstImg)
plt.show()