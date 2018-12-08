from PyQt5.QtCore import QThread, pyqtSignal


class SearchThread(QThread):
    finishedTrigger = pyqtSignal()
    putResultTrigger = pyqtSignal(dict)
    # PUT_INTERVAL = 1
    # OUTPUT_LIMIT = 100
    def __int__(self, searcher, *args):
        super(SearchThread, self).__init__()
    def initialize(self,  searcher, *args):
        self.searcher = searcher
        self.searchArgs = args
    def run(self):
        for item in self.searcher.search(*self.searchArgs):
            self.putResultTrigger.emit(item)
        self.sleep(1)
        # 循环完毕后发出信号
        self.finishedTrigger.emit()
    def quit(self):
        self.searcher.stopSearch()
        super(SearchThread, self).quit()