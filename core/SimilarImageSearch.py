import numpy as np
from PIL import Image
import os
from GUI.public.functions import config, getThumbCacheDir
import math
exts = ['jpg']
class SimilarImageSearch:
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
    def search(self, compareObj, searchRoot, scoreLimit,quantityLimit):
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

        fitImgList = []
        targetFeatureSum = np.sum(targetFeature)
        for item in imglist:
            score = int((1 - math.sqrt(sum((self.getFeature(item[0]) - targetFeature) ** 2)) / targetFeatureSum) * 100)
            if score >= scoreLimit:
                fitImgList.append((item[0], score))
        compareResults = sorted(fitImgList,key=lambda item: item[1], reverse=True)[:quantityLimit]

        results = []
        i = 0
        for item in compareResults:
            result = {}
            for field in self.fieldGetter:
                result[field] = self.fieldGetter[field](item[0])
            completePath = item[0]
            s = completePath.rfind("/")
            result["similarPercentage"] = "{0}%".format(item[1])
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