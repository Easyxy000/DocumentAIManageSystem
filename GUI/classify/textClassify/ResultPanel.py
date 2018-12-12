from GUI.classify.ActionDelegate import ActionDelegate
from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractResultPanel import AbstractResultPanel
from core.Field import Field
from functions import getBtn, DEFAULT


class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=ActionDelegate),
            Field("predict", "智能分类", formatMethod=self.getClassifyName)
        ],closeFields=["updatedTime","accessTime"])
        self.classifyName = None
        eventSystem.listen("setTextClassifyName", self.setClassifyNames, self)
    def setClassifyNames(self, names):
        self.classifyName = names
    def getClassifyName(self, id):
        return self.classifyName[id]
    def listenEvents(self):
        eventSystem.listen("finishTextClassify", self.finishClassify,self)
    def getBtns(self):

        return [
            getBtn(DEFAULT,"确定分类"),
        ]
    def finishClassify(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()