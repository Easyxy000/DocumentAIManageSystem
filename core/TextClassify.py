import codecs
import os
import jieba
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from core.File import File

exts = ["txt"]
class TextClassify(File):
    def __init__(self, closeFileds=None):
        super().__init__(closeFileds)
    def classify(self, trainPaths, predictPaths):
        # 创建label映射
        trainData = self.readTrainData(trainPaths)
        le, pipe = self.train(trainData)
        predictData = self.readPredictData(predictPaths)
        ans = pipe.predict(predictData["content"])
        result = []
        for path, predictClassId in zip(predictData["paths"], ans):
            fileData = self.buildData(path)
            fileData["predict"] = predictClassId
            result.append(fileData)
        return sorted(result, key=lambda x:x["predict"])
    def readTrainData(self, paths):
        # 读取所有文本文件
        files = []
        labels = []
        for i, path in enumerate(paths):
            for root, dirs, fs in os.walk(path, topdown=False):
                for file in fs:
                    if file[0] == ".": continue
                    ext = file.split(".")[-1].lower()
                    if ext not in exts: continue
                    files.append(os.path.join(root, file))
                    labels.append(i)
        data = {
            "paths": files,
            "label": labels,
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
    def train(self, data):
        """
        使用TFIDF+多项式模型对数据建模
        """
        pipe = Pipeline([("vect", CountVectorizer(token_pattern=r"(?u)\b\w+\b")),
                         ("tfidf", TfidfTransformer(norm=None, sublinear_tf=True)),
                         ("model", MultinomialNB())])
        le = LabelEncoder()
        Y = le.fit_transform(data["label"])
        pipe.fit(data["content"], Y)
        return le, pipe
# classify = TextClassify()
# results = TextClassify().classify(["/users/xushaojun/TextData2/train/{0}".format(category)
#                  for category in ["sport", "art", "computer", "economy"]],
#                   ["/users/xushaojun/TextData2/predict"])
# print(results)
