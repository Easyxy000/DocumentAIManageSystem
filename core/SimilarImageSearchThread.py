from PyQt5.QtCore import QThread, pyqtSignal

from core.SimilarImageSearch import SimilarImageSearch


class SimilarImageSearchThread(QThread):
    finishedTrigger = pyqtSignal(list)
    def __int__(self):
        super(SimilarImageSearchThread, self).__init__()
    def initialize(self, *args):
        self.args = args
    def run(self):
        searcher = SimilarImageSearch()
        results = searcher.search(*self.args)
        # 循环完毕后发出信号
        self.finishedTrigger.emit(results)