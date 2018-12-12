import numpy as np
from PIL import Image
import os
from functions import config, getThumbCacheDir
import math
exts = ['jpg','png','bpm','gif']
class SimilarImageSearch:
    def __init__(self):
        self.fieldGetter = {
            "fileSize" : lambda fileName : os.path.getsize(fileName),
            "createdTime" : lambda fileName : os.path.getctime(fileName),
            "updatedTime" : lambda fileName : os.path.getmtime(fileName),
            "accessTime": lambda fileName: os.path.getmtime(fileName),
        }
    def getFeature(self,src):
        im = np.array(Image.open(src).convert("RGB"))
        h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
        return h.flatten()
    def search(self, compareObj, searchRoot, limit=10):
        cacheDir = getThumbCacheDir("similar")
        thumbSize = config("search.similarSearchThumbSize")
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
        targetFeatureSum = np.sum(targetFeature)
        for item in compareResults:
            result = {}
            for field in self.fieldGetter:
                result[field] = self.fieldGetter[field](item[0])
            completePath = item[0]
            s = completePath.rfind("/")
            result["similarPercentage"] = "{0}%".format(int((1 - math.sqrt(item[1]) / targetFeatureSum) * 100))
            result["fileName"] = completePath[s + 1:]
            result["path"] = completePath[:s]
            thumbPath = os.path.join(cacheDir, "{0}.jpg".format(i))
            result["thumb"] = thumbPath
            results.append(result)


            im = Image.open(completePath)
            im.thumbnail(thumbSize)
            im.save(thumbPath, "JPEG")
            i += 1


        return results