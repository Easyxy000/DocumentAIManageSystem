# -*- coding: UTF-8 -*-
"""
此脚本用于展示如何使用朴素贝叶斯进行文本分类
所用语料来源于：复旦大学计算机信息与技术系国际数据库中心自然语言处理小组
由复旦大学李荣陆提供
"""


# 保证脚本与Python3兼容
import os
import jieba
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
def readData(dataPath, category, testRatio):
    """
    根据跟定的类别，读取数据，并将数据分为训练集和测试集
    """
    np.random.seed(2046)
    trainData = []
    testData = []
    labels = [i for i in os.listdir(dataPath) if i in category]
    # Windows下的存储路径与Linux并不相同
    for i in labels:
        for j in os.listdir("%s/%s" % (dataPath, i)):
            content = readContent("%s/%s/%s" % (dataPath, i, j))
            if np.random.random() <= testRatio:
                testData.append({"label": i, "content": content})
            else:
                trainData.append({"label": i, "content": content})
    trainData = pd.DataFrame(trainData)
    testData = pd.DataFrame(testData)
    return trainData, testData
def readContent(dataPath):
    with open(dataPath, "r", errors="ignore") as f:
        rawContent = f.read()
    content = ""
    for i in rawContent.split("\n"):
        try:
            content += i
        except UnicodeDecodeError:
            pass
    return content

def trainMultinomialNBWithTFIDF(data):
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
def trainModel(trainData, testData):
    # TFIDF+多项式模型
    le, pipe = trainMultinomialNBWithTFIDF(trainData)
    print(classification_report(
        le.transform(testData["label"]),
        pipe.predict(testData["content"]),
        target_names=le.classes_))

    return le, pipe
def textClassifierWithJieba(dataPaths):
    """
    使用第三方库jieba对文本进行分词，然后再进行分类
    """
    trainData, testData = readData(dataPaths, 0.3)
    trainData["content"] = trainData.apply(
        lambda x: " ".join(jieba.cut(x["content"], cut_all=True)), axis=1)
    testData["content"] = testData.apply(
        lambda x: " ".join(jieba.cut(x["content"], cut_all=True)), axis=1)
    le, pipe = trainModel(trainData, testData)

    return le, pipe


if __name__ == "__main__":

    category = ["C39-Sports","C3-Art"]
    le, pipe = textClassifierWithJieba(dataPaths)
    _docs = [" 关于古今中外流派和学派的描述", "浅论射击运动员在心理训练中注意品质的培养"]
    testDocs = [" ".join(jieba.cut(i, cut_all=True)) for i in _docs]
    pred = le.classes_[pipe.predict(testDocs)]
    print("Use TFIDF + multinomial naive Bayes: ")
    for doc, channel in zip(_docs, pred):
        print("{0} is {1}".format(doc, channel))
