from GUI.classify.ActionDelegate import ActionDelegate
from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractResultPanel import AbstractResultPanel
from GUI.public.ThumbDelegate import ThumbDelegate
from core.Field import Field
from functions import getBtn, DEFAULT, config, SUCCESS


class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        thumbSize = config("search.similarSearchThumbSize")
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=ActionDelegate),
            Field("predict", "智能分类", formatMethod=lambda i:"未命名分类{0}".format(i + 1)),
            Field("thumb", "缩略图", defaultSize=thumbSize[0], delegateClass=ThumbDelegate,
                  delegateParameters=(thumbSize,)),
        ],closeFields=["updatedTime","accessTime"])
    def listenEvents(self):
        eventSystem.listen("finishImageCluster", self.finishImageCluster,self)
    def getBtns(self):

        return [
            getBtn(SUCCESS,"设置分组名称并导出", self),
        ]
    def finishImageCluster(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()