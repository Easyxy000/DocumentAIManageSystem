from GUI.main.EventSystem import eventSystem
from GUI.repeatDetect.RepeatChildrenDelegate import RepeatChildrenDelegate
from GUI.public.AbstractResultPanel import AbstractResultPanel
from core.Field import Field
from functions import getBtn, DEFAULT, DANGER


class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=RepeatChildrenDelegate),
            Field("childrenCount", "重复数")
        ],closeFields=["accessTime","updatedTime"])
    def listenEvents(self):
        eventSystem.listen("finishRepeatSearch", self.finishSearch,self)
    def getBtns(self):

        return [
            getBtn(DEFAULT,"在结果中筛选"),
            getBtn(DANGER,"仅保留最新文件"),
            getBtn(DANGER, "仅保留最早文件")
        ]
    def finishSearch(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()