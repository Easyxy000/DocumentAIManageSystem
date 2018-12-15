from scipy.cluster.vq import whiten
from sklearn import svm

import numpy as np
from PIL import Image
import os

from core.ImageCluster import ImageCluster


def getFeature(src):
    im = np.array(Image.open(src))
    h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
    return h.flatten()
X = []
y = []
for i in range(4):
    for root, dirs, files in os.walk("/users/xushaojun/imageClassifyData/train/class{0}".format(i + 1), topdown=False):
        for file in files:
            if file[0] == ".": continue
            if "jpg" not in file:continue
            X.append(getFeature(os.path.join(root, file)))
            y.append(i + 1)
X = np.array(X)
y = np.array(y)
X_validate = []
k = 5
imglist = []

predictY = []
for root, dirs, files in os.walk("/users/xushaojun/imageClassifyData/test", topdown=False):
    for file in files:
        if file[0] == ".": continue
        if "jpg" not in file: continue
        imglist.append(os.path.join(root, file))
        f = getFeature(os.path.join(root, file))
        distances = np.sum((f - X)**2,axis=1)
        ys = distances.argsort()[:5]
        ans = np.bincount(y[ys]).argmax()
        predictY.append(ans)


for img, i in zip(imglist, predictY):
    print("{0} is group {1}".format(img, i))