import os
from PyQt5.QtCore import QThread, pyqtSignal

from core.ImageClassify import ImageClassify
from core.TextClassify import TextClassify


class ImageClassifyThread(QThread):
    finishedTrigger = pyqtSignal(list)
    def __int__(self):
        super(ImageClassifyThread, self).__init__()
    def initialize(self, classifyDirRoot, predictDirs, closeFields=None):
        self.classifyDirRoot = classifyDirRoot
        self.predictDirs = predictDirs
        self.closeFields = closeFields
    def run(self):
        self.searcher = ImageClassify(self.closeFields)

        classifyDirs = []
        for root, dirs, fs in os.walk(self.classifyDirRoot, topdown=False):
            for dir in dirs:
                classifyDirs.append(os.path.join(root, dir))
        results = self.searcher.classify(classifyDirs, self.predictDirs)

        # 循环完毕后发出信号
        self.finishedTrigger.emit(sorted(results, key=lambda x: x["predict"]))