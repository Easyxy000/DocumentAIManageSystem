from PyQt5.QtWidgets import QPushButton

from GUI.EventSystem import eventSystem
from GUI.components.ActionDelegate import ActionDelegate
from GUI.components.TableView import TableView
from core.Field import Field


class SearchResult(TableView):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", editable=True, delegateClass=ActionDelegate),
        ])
    def createBtnGroup(self):
        similarSearchBtn = QPushButton("相似图片搜索", self)
        similarSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "similarImageSearch"))

        return [
            QPushButton("在结果中筛选", self),
            similarSearchBtn
        ]