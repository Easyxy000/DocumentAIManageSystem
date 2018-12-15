import numpy as np
from PIL import Image
import os

from cv2.cv2 import imshow


def getFeature(src):
    im = np.array(Image.open(src))
    h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
    return h.flatten()
exts = ['jpg','png','bpm','gif']
class SimilarImageSearcher:
    def __init__(self):
        pass
    def search(self, compareObj, searchRoot, limit=10):
        imglist = []
        for root, dirs, files in os.walk(searchRoot, topdown=False):
            for file in files:
                ext = file[file.rfind(".") + 1:].lower()
                if ext not in exts: continue
                completePath = os.path.join(root,file)
                imglist.append([completePath, None])

        targetFeature = getFeature(compareObj)
        for item in imglist:
            item[1] = sum((getFeature(item[0]) - targetFeature) ** 2)
        result = sorted(imglist,key=lambda item: item[1])[:limit]
        return result
# result = ImageClassify().search("/users/xushaojun/flickr-sunsets-small/3481780431_052b1d4bdb.jpg", "/users/xushaojun/flickr-sunsets-small")
# for item in result:
#     print("{0} : {1}".format(item[0], item[1]))