from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from GUI.classify.imageCluster.ImageClusterTab import ImageClusterTab
from GUI.classify.textClassify.ClassifyTextTab import ClassifyTextTab
from GUI.classify.textCluster.ClusterTextTab import ClusterTextTab
from GUI.search.similar.SimilarImageSearchTab import SimilarImageSearchTab
from GUI.search.normal.NormalFileSearchTab import NormalFileSearchTab
from GUI.repeatDetect.MainContentTabCheck import MainContentTabCheck

from GUI.main.EventSystem import eventSystem
from GUI.setting.SettingTab import SettingTab
from functions import config


class MainContent(QWidget):
    def __init__(self, parent, size, initId):
        super().__init__(parent)
        self.resize(*size)
        eventSystem.listen("changeTab", self.changeTab, self)
        self.constructors = {
            "normalSearch" : NormalFileSearchTab,
            "similarImageSearch": SimilarImageSearchTab,
            "repeatDetect" : MainContentTabCheck,
            "textClassify" : ClassifyTextTab,
            "textCluster": ClusterTextTab,
            "imageCluster" : ImageClusterTab,
            "setting": SettingTab,

        }
        self.idMenuMap = {
            "similarImageSearch": "search",
            "normalSearch" : "search",
            "textClassify" : "classify",
            "textCluster" : "classify",
            "imageCluster" : "classify"
        }
        self.active = None
        self.tabs = {}
        self.changeTab(initId)
        self.show()
    def changeTab(self, tabId):
        if self.active is not None:
            print("hide {0}".format(self.active.id))
            self.active.hide()

        w, h = self.size().width(), self.size().height() - config("gui.mainContentTabMarginBottom")
        self.tabs.setdefault(tabId, self.constructors[tabId](self, QSize(w, h)))
        current = self.tabs[tabId]
        current.show()
        self.active = current
        print("show {0}".format(tabId))

        if tabId in self.idMenuMap:
            tabId = self.idMenuMap[tabId]

        eventSystem.dispatch("selectedMenu", tabId)