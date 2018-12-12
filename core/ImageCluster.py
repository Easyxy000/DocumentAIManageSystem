 # -*- coding: utf-8 -*-
from PIL import Image
from scipy.cluster.vq import *
import numpy as np
import os
import pylab
from core.File import File
from functions import getThumbCacheDir, config
exts = ["jpg"]
class ImageCluster(File):
    def run(self, path, k):
        immatrix, imgList = self.getFeatureImmatrix(path)
        V = self.getV(immatrix, len(imgList))
        centroids, distortion, features = self.cluster(V, k)
        code, distance = self.getClusterResult(features, centroids)
        cacheDir = getThumbCacheDir("imageCluster")
        thumbSize = config("search.similarSearchThumbSize")

        result = []
        i = 0
        for img, classify in zip(imgList, code):
            file = self.buildData(img)
            thumbPath = os.path.join(cacheDir, "{0}.jpg".format(i))
            file["thumb"] = thumbPath
            file["predict"] = classify
            im = Image.open(img)
            im.thumbnail(thumbSize)
            im.save(thumbPath, "JPEG")
            result.append(file)
            i += 1
        return sorted(result, key=lambda x:x["predict"])
        # self.printClusterResult(imgList, k, code)
    def getFeatureImmatrix(self, path):
        imgList = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        features = np.zeros([len(imgList), 512])
        for i, f in enumerate(imgList):
            im = np.array(Image.open(f))
            # multi-dimensional histogram
            h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
            features[i] = h.flatten()
        return np.array(features), imgList
    def getV(self, immatrix, imgCount):
        V, S, immean = self.pca(np.array(immatrix))
        projected = np.array([np.dot(V[[0, 1]], immatrix[i] - immean) for i in range(imgCount)])  # P131 Fig6-3左图
        n = len(projected)
        S = np.array([[np.sqrt(sum((projected[i] - projected[j]) ** 2))
                    for i in range(n)] for j in range(n)], 'f')
        rowsum = np.sum(S, axis=0)
        D = np.diag(1 / np.sqrt(rowsum))
        I = np.identity(n)
        L = I - np.dot(D, np.dot(S, D))
        U, sigma, V = np.linalg.svd(L)
        return V
    def cluster(self, V, k):
        features = np.array(V[:k]).T
        features = whiten(features)
        centroids, distortion = kmeans(features, k)
        return centroids, distortion, features
    def getClusterResult(self, features, centroids):
        code, distance = vq(features, centroids)
        return code, distance
    def pca(self, X):
        num_data, dim = X.shape

        mean_X = X.mean(axis=0)
        X = X - mean_X

        if dim > num_data:
            M = np.dot(X, X.T)  #
            e, EV = np.linalg.eigh(M)
            tmp = np.dot(X.T, EV).T
            V = tmp[::-1]
            S = np.sqrt(e)[::-1]
            for i in range(V.shape[1]):
                V[:, i] /= S
        else:
            U, S, V = np.linalg.svd(X)
            V = V[:num_data]
        return V, S, mean_X
    def center(self, X):
        n, m = X.shape
        if n != m:
            raise Exception('Matrix is not square.')
        colsum = X.sum(axis=0) / n
        rowsum = X.sum(axis=1) / n
        totalsum = X.sum() / (n ** 2)
        Y = np.array([[X[i, j] - rowsum[i] - colsum[j] + totalsum for i in range(n)] for j in range(n)])
        return Y
    def printClusterResult(self, imglist, k, code):
        for c in range(k):
            ind = np.where(code == c)[0]
            pylab.figure()
            pylab.gray()
            for i in range(pylab.minimum(len(ind), 39)):
                im = Image.open(imglist[ind[i]])
                pylab.subplot(4, 10, i + 1)
                pylab.imshow(pylab.array(im))
                pylab.axis('equal')
                pylab.axis('off')
        pylab.show()
# results = ImageCluster().run("/users/xushaojun/imageClusterData", 3)
# for item in results:
#     print(item)