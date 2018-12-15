from PyQt5.QtWidgets import QFileDialog

from GUI.classify.ActionDelegate import ActionDelegate
from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractResultPanel import AbstractResultPanel
from GUI.public.ThumbDelegate import ThumbDelegate
from core.Field import Field
from GUI.public.functions import getBtn, config, SUCCESS, infoDialog
import  os, shutil

class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        thumbSize = config("search.similarSearchThumbSize")
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=ActionDelegate),
            Field("predict", "智能分类", formatMethod=lambda i:"未命名分类{0}".format(i + 1)),
            Field("thumb", "缩略图", defaultSize=thumbSize[0], delegateClass=ThumbDelegate,
                  delegateParameters=(thumbSize,)),
        ],closeFields=["updatedTime","accessTime"])
    def setCluserCount(self, n):
        self.classCount = int(n)
    def listenEvents(self):
        eventSystem.listen("finishImageCluster", self.finishImageCluster,self)
        eventSystem.listen("setImageCluster", self.setCluserCount, self)
    def getBtns(self):
        confirmClusterBtn = getBtn(SUCCESS,"确定并导出")
        confirmClusterBtn.clicked.connect(self.output)
        return [
            confirmClusterBtn,
        ]
    def output(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        files = self.model.files
        dirs = []
        for i in range(self.classCount):
            dir = os.path.join(fname, "未命名分类{0}".format(i + 1))
            os.mkdir(dir)
            dirs.append(dir)

        for file in files:
            shutil.move(os.path.join(file["path"], file["fileName"]), dirs[file["predict"]])
        infoDialog("您已成功导出分类", self)
    def finishImageCluster(self, results):
        self.model.load(results)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()