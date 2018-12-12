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
    def __init__(self):
        super().__init__(None)
    def search(self, paths):
        # 创建label映射
        self.labelMap = dict([(path, i) for i, path in enumerate(paths)])

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

        # 拆分训练集 测试集
        path_train, path_test, y_train, y_test = train_test_split(files, labels, test_size=0.2)

        allData = {}
        for key, paths, labels in zip(
                ("train", "test"),
                (path_train, path_test),
                (y_train, y_test)
        ):
            dataGroup = {"paths" : paths, "label" : labels}
            dataGroup["content"] = [" ".join(jieba.cut(self.readContent(path),cut_all=True)) for path in paths]
            allData[key] = pd.DataFrame(dataGroup)
        self.allData = allData
        self.le, self.pipe = self.trainMultinomialNBWithTFIDF(allData["train"])

        # self.printTest()
        ans = self.pipe.predict(allData["train"]["content"])

        print("labels")
        for label, a in zip(allData["train"]["label"], ans):
            print("label is {}, ans is {}".format(label, a))
    def readContent(self, path):
        try:
            f = codecs.open(path, "r+", encoding='gbk')
            lines = [line for line in f.readlines()]
            return "\n".join(lines)
        except:
            print("error file:{0}".format(path))
    def trainMultinomialNBWithTFIDF(self, data):
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
classify = TextClassify()
# generator = jieba.cut(classify.readContent("/users/xushaojun/TextData1/C11-Space/C11-Space1095.txt"))
# print(" ".join(generator))
classify.search(["/users/xushaojun/TextData2/train/{0}".format(category)
                 for category in ["sport", "art"]])