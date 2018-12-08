import os
import numpy as np
from PIL import Image


def getFeature(src):
    im = np.array(Image.open(src))
    # multi-dimensional histogram
    h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
    return h.flatten()
l = 3


src = []
for root, dirs, files in os.walk("/users/xushaojun/test2", topdown=False):
    for file in files:
        if file[0] ==".": continue
        src.append(os.path.join(root , file))

features = [ getFeature(item) for item in src]
for i in range(len(src)):
    print("\n\nthe similar of {0}".format(src[i]))
    scores = [(sum((features[i] - features[j]) ** 2), j) for j in range(len(src))]
    k = 0
    for item in sorted(scores, key=lambda item: item[0])[:5]:
        print("the {0}th similar img is {1}".format(k, src[item[1]]))
        k += 1
