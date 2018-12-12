import codecs
import os
import jieba
import numpy as np
import pandas as pd
from sklearn.cluster import Birch, KMeans, DBSCAN, SpectralClustering
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report, silhouette_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from core.File import File

exts = ["txt"]
class TextCluster(File):
    def __init__(self, closeFileds=None):
        super().__init__(closeFileds)
    def run(self, trainPaths,n):
        # 创建label映射
        trainData = self.readTrainData(trainPaths)
        ans = self.train(trainData,n)
        result = []
        for path, predictClassId in zip(trainData["paths"], ans):
            fileData = self.buildData(path)
            fileData["predict"] = predictClassId
            result.append(fileData)
        return sorted(result, key=lambda x:x["predict"])
    def readTrainData(self, path):
        # 读取所有文本文件
        files = []
        for file in os.listdir(path):
            if file[0] == ".": continue
            ext = file.split(".")[-1].lower()
            if ext not in exts: continue
            files.append(os.path.join(path, file))
        data = {
            "paths": files,
            "content": [
                " ".join(jieba.cut(self.readContent(file), cut_all=True))
                for file in files
            ]
        }
        return data
    def readPredictData(self, paths):
        # 读取所有文本文件
        files = []
        for i, path in enumerate(paths):
            for root, dirs, fs in os.walk(path, topdown=False):
                for file in fs:
                    if file[0] == ".": continue
                    ext = file.split(".")[-1].lower()
                    if ext not in exts: continue
                    files.append(os.path.join(root, file))
        data = {
            "paths": files,
            "content":  [
                " ".join(jieba.cut(self.readContent(file), cut_all=True))
                for file in files
            ]
        }
        return data
    def readContent(self, path):
        try:
            f = codecs.open(path, "r+", encoding='gbk')
            lines = [line for line in f.readlines()]
            return "\n".join(lines)
        except:
            print("error file:{0}".format(path))
    def train(self, data,n):
        vectorizer = CountVectorizer()
        # 该类会统计每个词语tfidf权值
        transformer = TfidfTransformer()
        # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        tfidf = transformer.fit_transform(vectorizer.fit_transform(data["content"]))
        weight = tfidf.toarray()
        V = PCA(n_components=1600).fit_transform(weight)
        y = KMeans(n_clusters=n).fit_predict(V)
        print(silhouette_score(weight, y))

        return y
# classify = TextClassify()
# results = TextClassify().classify(["/users/xushaojun/TextData2/train/{0}".format(category)
#                  for category in [ "art", "computer", "economy"]])