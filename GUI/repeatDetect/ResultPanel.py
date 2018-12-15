from GUI.main.EventSystem import eventSystem
from GUI.repeatDetect.RepeatChildrenDelegate import RepeatChildrenDelegate
from GUI.public.AbstractResultPanel import AbstractResultPanel
from core.Field import Field
from GUI.public.functions import getBtn, DEFAULT, DANGER, PRIMARY
import os

class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=RepeatChildrenDelegate),
            Field("childrenCount", "重复数")
        ],closeFields=["accessTime","updatedTime"])
    def listenEvents(self):
        eventSystem.listen("finishRepeatSearch", self.finishSearch,self)
    def getBtns(self):
        removeExcluseLatestBtn = getBtn(DANGER, "仅保留最新文件")
        removeExcluseLatestBtn.clicked.connect(lambda : self.removeExceptOne(reverse=True))

        removeExcluseEarlestBtn = getBtn(DANGER, "仅保留最早文件")
        removeExcluseEarlestBtn.clicked.connect(lambda : self.removeExceptOne(reverse=False))
        return [
            removeExcluseLatestBtn,
            removeExcluseEarlestBtn
        ]
    def removeExceptOne(self, reverse=False):
        self.model.beginResetModel()
        removePaths = []
        for group in self.model.files:
            group["children"] = sorted(group["children"], key=lambda x: x["createdTime"], reverse=reverse)
            removePaths += [os.path.join(item["path"], item["fileName"]) for item in group["children"][1:]]
            group["children"] = group["children"][:1]
            group["childrenCount"] = 1
        for item in removePaths:
            os.remove(item)
        print("success remove {0} items".format(len(removePaths)))
        self.model.endResetModel()
    def finishSearch(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
    def _getBtns(self):
        submitBtn = getBtn(PRIMARY, "开始搜索")
        submitBtn.clicked.connect(lambda : eventSystem.dispatch("researchRepeatDetect"))
        return self.getBtns() + [submitBtn]