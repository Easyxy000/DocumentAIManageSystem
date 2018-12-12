from PyQt5.QtCore import QThread, pyqtSignal

from core.RepeatFileSearch import RepeatFileSearch


class RepeatFileSearchThread(QThread):
    finishedTrigger = pyqtSignal(list)
    def __int__(self):
        super(RepeatFileSearchThread, self).__init__()
    def initialize(self, searchRoot, closeFields=None):
        self.searchRoot = searchRoot
        self.searcher = None
        self.closeFields = closeFields
    def run(self):
        self.searcher = RepeatFileSearch(self.closeFields)
        results = self.searcher.search( self.searchRoot)
        # 循环完毕后发出信号
        self.finishedTrigger.emit(results)