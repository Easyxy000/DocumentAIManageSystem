from PyQt5.QtWidgets import QWidget, QLabel

from GUI.search.SimilarImageSearch import SimilarImageSearch
from functions import config
from GUI.index.MainContentTabIndex import MainContentTabIndex
from GUI.search.MainContentTabSearch import MainContentTabSearch
from GUI.check.MainContentTabCheck import MainContentTabCheck
from GUI.setting.MainContentTabSetting import MainContentTabSetting

from GUI.EventSystem import eventSystem
class MainContent(QWidget):
    def __init__(self, parent, size, initId):
        super().__init__(parent)
        self.resize(*size)
        eventSystem.listen("changeTab", self.changeTab, self)
        self.constructors = {
            "index" : MainContentTabIndex,
            "search" : MainContentTabSearch,
            "check" : MainContentTabCheck,
            "setting" : MainContentTabSetting,
            "similarImageSearch" : SimilarImageSearch
        }
        self.active = None
        self.tabs = {}
        self.changeTab(initId)
        self.show()
    def changeTab(self, tabId):
        if self.active is not None:
            print("hide {0}".format(self.active.id))
            self.active.hide()
        self.tabs.setdefault(tabId, self.constructors[tabId](self, self.size()))
        current = self.tabs[tabId]
        current.show()
        self.active = current
        print("show {0}".format(tabId))