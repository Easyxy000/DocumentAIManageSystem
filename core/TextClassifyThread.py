import os
from PyQt5.QtCore import QThread, pyqtSignal

from core.TextClassify import TextClassify


class TextClassifyThread(QThread):
    finishedTrigger = pyqtSignal(list)
    def __int__(self):
        super(TextClassifyThread, self).__init__()
    def initialize(self, classifyDirRoot, predictDirs, closeFields=None):
        self.classifyDirRoot = classifyDirRoot
        self.predictDirs = predictDirs
        self.closeFields = closeFields
    def run(self):
        self.searcher = TextClassify(self.closeFields)

        classifyDirs = []
        for root, dirs, fs in os.walk(self.classifyDirRoot, topdown=False):
            for dir in dirs:
                classifyDirs.append(os.path.join(root, dir))
        results = self.searcher.classify(classifyDirs, self.predictDirs)

        # results = [{'fileSize': 7729, 'createdTime': 1544424633.0, 'updatedTime': 1537490053.0, 'accessTime': 1537490053.0, 'fileName': 'C19-Computer0078.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'computer'}, {'fileSize': 11422, 'createdTime': 1544424633.0, 'updatedTime': 1537490053.0, 'accessTime': 1537490053.0, 'fileName': 'C19-Computer0080.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'computer'}, {'fileSize': 5045, 'createdTime': 1544424634.0, 'updatedTime': 1537490053.0, 'accessTime': 1537490053.0, 'fileName': 'C19-Computer0082.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'computer'}, {'fileSize': 8443, 'createdTime': 1544424634.0, 'updatedTime': 1537490053.0, 'accessTime': 1537490053.0, 'fileName': 'C19-Computer0084.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'computer'}, {'fileSize': 12738, 'createdTime': 1544424634.0, 'updatedTime': 1537490053.0, 'accessTime': 1537490053.0, 'fileName': 'C19-Computer0086.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'computer'}, {'fileSize': 7484, 'createdTime': 1544415366.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C3-Art0039.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'art'}, {'fileSize': 28927, 'createdTime': 1544415366.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C3-Art0041.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'art'}, {'fileSize': 26953, 'createdTime': 1544415367.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C3-Art0043.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'art'}, {'fileSize': 2556, 'createdTime': 1544424659.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C34-Economy0028.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'economy'}, {'fileSize': 3653, 'createdTime': 1544424659.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C34-Economy0030.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'economy'}, {'fileSize': 8591, 'createdTime': 1544424659.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C34-Economy0032.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'economy'}, {'fileSize': 6644, 'createdTime': 1544424659.0, 'updatedTime': 1537490054.0, 'accessTime': 1537490054.0, 'fileName': 'C34-Economy0038.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'economy'}, {'fileSize': 10789, 'createdTime': 1544415394.0, 'updatedTime': 1537490055.0, 'accessTime': 1537490055.0, 'fileName': 'C39-Sports0059.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'sport'}, {'fileSize': 4802, 'createdTime': 1544415394.0, 'updatedTime': 1537490055.0, 'accessTime': 1537490055.0, 'fileName': 'C39-Sports0060.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'sport'}, {'fileSize': 11722, 'createdTime': 1544415394.0, 'updatedTime': 1537490055.0, 'accessTime': 1537490055.0, 'fileName': 'C39-Sports0062.txt', 'path': '/users/xushaojun/TextData2/predict', 'predict': 'sport'}]

        # 循环完毕后发出信号
        self.finishedTrigger.emit(sorted(results, key=lambda x: x["predict"]))