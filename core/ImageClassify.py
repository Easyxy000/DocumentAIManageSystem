import numpy as np
from PIL import Image
import os
import math
from core.File import File
from GUI.public.functions import config, getThumbCacheDir
exts = ['jpg','png','bpm','gif','jpeg']
class ImageClassify(File):
    def getFeature(self,src):
        img = Image.open(src)
        h, edges = np.histogramdd(np.array(img).reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
        return h.flatten()
    def classify(self, categoriedDirs, classifyDir):
        X = []
        y = []
        for i,category in enumerate(categoriedDirs):
            for root, dirs, files in os.walk(category, topdown=False):
                for file in files:
                    ext = file[file.rfind(".") + 1:].lower()
                    if ext not in exts: continue
                    completePath = os.path.join(root, file)
                    X.append(self.getFeature(completePath))
                    y.append(i)
        X = np.array(X)
        y = np.array(y)
        k = len(y) // len(categoriedDirs)
        cacheDir = getThumbCacheDir("imageClassify")
        thumbSize = config("search.similarSearchThumbSize")
        results = []
        for root, dirs, files in os.walk(classifyDir, topdown=False):
            for i,file in enumerate(files):
                ext = file[file.rfind(".") + 1:].lower()
                if ext not in exts: continue
                completePath = os.path.join(root, file)
                f = np.array(self.getFeature(completePath))
                distances = np.sum((f - X) ** 2, axis=1)
                ys = distances.argsort()[:k]
                # w = np.zeros(len(categoriedDirs))
                # for j in ys:
                #     w[y[j]] += self.gaussian(distances[j])
                # ans = w.argmax()
                ans = np.bincount(y[ys]).argmax()

                thumbPath = os.path.join(cacheDir, "{0}.jpg".format(i))
                im = Image.open(completePath)
                im.thumbnail(thumbSize)
                im.save(thumbPath, "JPEG")

                file = self.buildData(completePath)
                file["predict"] = ans
                file["thumb"] = thumbPath
                results.append(file)
        return results
    def gaussian(self, dist, sigma=10.0):
        return math.e ** (-dist**2/(2*sigma**2))