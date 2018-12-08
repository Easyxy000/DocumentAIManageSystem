from PyQt5.QtWidgets import QPushButton

from GUI.EventSystem import eventSystem
from GUI.components.ActionDelegate import ActionDelegate
from GUI.components.TableView import TableView
from GUI.components.ThumbDelegate import ThumbDelegate
from core.Field import Field


class SimilarSearchResult(TableView):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", delegateClass=ActionDelegate),
            Field("thumb", "缩略图", delegateClass=ThumbDelegate),
        ])
        eventSystem.listen("finishedSimilarImageSearch", self.getResults, self)
    def getResults(self, results):
        self.model.load(results)
    def createBtnGroup(self):
        similarSearchBtn = QPushButton("一般文件搜索", self)
        similarSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "search"))

        return [
            similarSearchBtn
        ]