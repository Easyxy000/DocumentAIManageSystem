from GUI.classify.ActionDelegate import ActionDelegate
from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractResultPanel import AbstractResultPanel
from core.Field import Field
from GUI.public.functions import getBtn, DEFAULT, infoDialog
import os, shutil

class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=ActionDelegate),
            Field("predict", "智能分类", formatMethod=self.getClassifyName)
        ],closeFields=["updatedTime","accessTime"])
        self.className = None
        self.classDirs = None
    def getClassifyName(self, id):
        return self.className[id]
    def listenEvents(self):
        eventSystem.listen("finishTextClassify", self.finishClassify,self)
        eventSystem.listen("setTextClass", self.setTextClass, self)
    def setTextClass(self, names, dirs):
        self.className = names
        self.classDirs = dirs
    def getBtns(self):
        comfirmClassifyBtn = getBtn(DEFAULT,"确定分类")
        comfirmClassifyBtn.clicked.connect(self.comfirmClassify)
        return [
            comfirmClassifyBtn
        ]
    def comfirmClassify(self):
        files = self.model.files
        self.model.beginResetModel()
        for file in files:
            targetPath = self.classDirs[file["predict"]]
            shutil.move(os.path.join(file["path"], file["fileName"]), targetPath)
            file["path"] = targetPath
        infoDialog("已成功将所有文件移动到对应分类下的文件夹", self)
        self.model.endResetModel()
    def finishClassify(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()