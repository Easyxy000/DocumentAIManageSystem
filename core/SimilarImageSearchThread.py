from PyQt5.QtCore import QThread, pyqtSignal

from core.SimilarImageSearcher import SimilarImageSearcher


class SimilarImageSearchThread(QThread):
    finishedTrigger = pyqtSignal(list)
    def __int__(self, searcher, *args):
        super(SimilarImageSearchThread, self).__init__()
    def initialize(self,  src, searchRoot):
        self.src = src
        self.searchRoot = searchRoot
        self.searcher = None
    def run(self):
        self.searcher = SimilarImageSearcher()
        results = self.searcher.search(self.src, self.searchRoot)
        # 循环完毕后发出信号
        self.finishedTrigger.emit(results)