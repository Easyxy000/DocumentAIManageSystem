from PyQt5.QtCore import QThread, pyqtSignal

from core.ImageCluster import ImageCluster
from core.SimilarImageSearch import SimilarImageSearch


class ImageClusterThread(QThread):
    finishedTrigger = pyqtSignal(list)
    def __int__(self, closeFileds=None):
        super(ImageClusterThread, self).__init__()
    def initialize(self, clusterDir, cluster_n, closeFileds=None):
        self.clusterDir = clusterDir
        self.cluster_n = cluster_n
        self.closeFileds = closeFileds
    def run(self):
        self.searcher = ImageCluster(self.closeFileds)
        results = self.searcher.run(self.clusterDir, int(self.cluster_n))
        # 循环完毕后发出信号
        self.finishedTrigger.emit(results)