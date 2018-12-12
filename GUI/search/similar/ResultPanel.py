from GUI.main.EventSystem import eventSystem
from GUI.public.ActionDelegate import ActionDelegate
from GUI.public.AbstractResultPanel import AbstractResultPanel
from GUI.public.ThumbDelegate import ThumbDelegate
from core.Field import Field
from functions import getThumbCacheDir, config, getBtn, INFO


class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        cacheDir = getThumbCacheDir("similar")
        thumbSize = config("search.similarSearchThumbSize")
        super().__init__(p, size,[
            Field("action", "操作",hasValue=False, delegateClass=ActionDelegate),
            Field("thumb", "缩略图",defaultSize=thumbSize[0], delegateClass=ThumbDelegate,delegateParameters=(thumbSize, )),
            Field("similarPercentage", "相似度")
        ],closeFields=["updatedTime","accessTime"])
        eventSystem.listen("finishedSimilarImageSearch", self.getResults, self)
        self.setObjectName("similarImageSearchResult")
        self.tableView.verticalHeader().setDefaultSectionSize(thumbSize[1])
    def getResults(self, results):
        self.model.load(results)
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()
    def getBtns(self):
        similarSearchBtn = getBtn(INFO,"一般文件搜索")
        similarSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "normalSearch"))

        return [
            similarSearchBtn
        ]