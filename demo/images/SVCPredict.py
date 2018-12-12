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
limit = 1
for i in range(3):
    for root, dirs, files in os.walk("/users/xushaojun/data3/train/000{0}".format(i), topdown=False):
        i = 0
        for file in files:
            if file[0] == ".": continue
            if i > limit:break
            X.append(getFeature(os.path.join(root, file)))
            y.append(i)
            i += 1
V,S, m = ImageCluster().pca(np.array(X).T)
V = V[:50]
X = np.array([np.dot(V, f - m) for f in X])
# features = np.array(V)
# features = whiten(features)
clf = svm.SVC()  # class
clf.fit(X, y)  # training the svc model

X_validate = []
imglist = []
for root, dirs, files in os.walk("/users/xushaojun/data3/test", topdown=False):
    for file in files:
        if file[0] ==".": continue
        imglist.append(file)
        X_validate.append(getFeature(os.path.join(root, file)))


ans = clf.predict(X_validate)

for img, predictY in zip(imglist, ans):
    print("{0} is group {1}".format(img, predictY + 1))