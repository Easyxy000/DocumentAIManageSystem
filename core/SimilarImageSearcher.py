import numpy as np
from PIL import Image
import os

from cv2.cv2 import imshow


exts = ['jpg','png','bpm','gif']
class SimilarImageSearcher:
    def __init__(self):
        self.fieldGetter = {
            "fileSize" : lambda fileName : os.path.getsize(fileName),
            "createdTime" : lambda fileName : os.path.getctime(fileName),
            "updatedTime" : lambda fileName : os.path.getmtime(fileName),
            "accessTime": lambda fileName: os.path.getmtime(fileName),
        }
    def getFeature(self,src):
        im = np.array(Image.open(src))
        h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
        return h.flatten()
    def search(self, compareObj, searchRoot, limit=10, thumbSize=(100,40)):
        imglist = []
        for root, dirs, files in os.walk(searchRoot, topdown=False):
            for file in files:
                ext = file[file.rfind(".") + 1:].lower()
                if ext not in exts: continue
                completePath = os.path.join(root,file)
                imglist.append([completePath, None])

        targetFeature = self.getFeature(compareObj)
        for item in imglist:
            item[1] = sum((self.getFeature(item[0]) - targetFeature) ** 2)
        compareResults = sorted(imglist,key=lambda item: item[1])[:limit]

        results = []
        i = 0
        for item in compareResults:
            result = {}
            for field in self.fieldGetter:
                result[field] = self.fieldGetter[field](item[0])
            completePath = item[0]
            s = completePath.rfind("/")
            result["fileName"] = completePath[s + 1:]
            result["path"] = completePath[:s]
            results.append(result)

            im = Image.open(completePath)
            im.thumbnail(thumbSize)
            im.save("cache/{0}.jpg".format(i), "JPEG")
            i += 1


        return results
# result = SimilarImageSearcher().search("/users/xushaojun/flickr-sunsets-small/3481780431_052b1d4bdb.jpg", "/users/xushaojun/flickr-sunsets-small")
# for item in result:
#     print("{0} : {1}".format(item[0], item[1]))