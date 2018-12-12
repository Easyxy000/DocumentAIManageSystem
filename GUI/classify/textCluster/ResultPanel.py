from GUI.classify.ActionDelegate import ActionDelegate
from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractResultPanel import AbstractResultPanel
from core.Field import Field
from functions import getBtn, DEFAULT, SUCCESS


class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=ActionDelegate),
            Field("predict", "智能分类", formatMethod=lambda i:"未命名分类{0}".format(i + 1)),
        ],closeFields=["updatedTime","accessTime"])
        self.classifyName = None
    def setClassifyNames(self, names):
        self.classifyName = names
    def getClassifyName(self, id):
        return self.classifyName[id]
    def listenEvents(self):
        eventSystem.listen("finishTextCluster", self.finishClassify,self)
    def getBtns(self):

        return [
            getBtn(SUCCESS,"设定分类名称并导出"),
        ]
    def finishClassify(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()