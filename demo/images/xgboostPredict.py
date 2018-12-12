# ================基于Scikit-learn接口的回归================
import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error   # 准确率
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from PIL import Image
import os

from cv2.cv2 import imshow


def getFeature(src):
    im = np.array(Image.open(src).convert("RGB"))
    h, edges = np.histogramdd(im.reshape(-1, 3), 8, normed=True, range=[(0, 255), (0, 255), (0, 255)])
    return h.flatten()
import os
def train(X, y):
    # XGBoost训练过程
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    param_grid = {
        'max_depth': range(3, 10, 2),
        'min_child_weight': range(1, 6, 2)
    }

    model = GridSearchCV(estimator=xgb.XGBClassifier(
        max_depth=5,
        learning_rate=0.1,
        n_estimators=160,
        silent=True,
        objective='multi:softmax',

    ), param_grid=param_grid, cv=5)
    model.fit(X_train, y_train)

    # 对测试集进行预测
    ans = model.predict(X_test)
    return mean_squared_error(ans, y_test), model

# classfiyData
X = []
Y = []
for i in range(3):
    for root, dirs, files in os.walk("/users/xushaojun/data3/train/000{0}".format(i + 1), topdown=False):
        for file in files:
            if file[0] == ".": continue

            X.append(getFeature(os.path.join(root, file)))
            Y.append(i)

score, model = train(X, Y)

X_validate = []
imglist = []
for root, dirs, files in os.walk("/users/xushaojun/data3/test", topdown=False):
    for file in files:
        if file[0] ==".": continue
        imglist.append(file)
        X_validate.append(getFeature(os.path.join(root, file)))

ans = model.predict(X_validate)

for img, predictY in zip(imglist, ans):
    print("{0} is group {1}".format(img, predictY + 1))