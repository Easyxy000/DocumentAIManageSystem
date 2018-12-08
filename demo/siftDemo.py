import cv2
import numpy as np


img = cv2.imread('images/logo.png')
sift = cv2.xfeatures2d.SURF_create()


kp = sift.detect(img,None)#找到关键点

img=cv2.drawKeypoints(img,kp,img)#绘制关键点

cv2.imshow('sp',img)
cv2.waitKey(0)