from PyQt5.QtWidgets import QLineEdit

from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from GUI.public.FormItem import FormItem
from core.TextClassifyThread import TextClassifyThread
from core.TextClusterThread import TextClusterThread
from functions import getBtn, PRIMARY, INFO, SUCCESS


class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.form = {}
        self.checkedType = {}
        self.searcher = None
        self.searching = False
        self.initUI("文本自动分类",topMargin=120, bottomMargin=200)
        eventSystem.listen("stopSearch", self.stopSearch, self)
    def createFieldGroup(self):
        self.createGroup(self.createRootDirctoryChoose, "已归类文件夹", 'classifyDirs')
        self.createGroup(self.createClusterN, "分类个数", 'cluster_n')
    def createClusterN(self):
        edit = QLineEdit(self)
        return FormItem(edit, getVal=edit.text)
    def stopSearch(self):
        if self.worker is not None:
            self.worker.quit()
            self.worker.wait()
    def getBtns(self):
        submitButton = getBtn(PRIMARY, "开始归类整理", self)
        submitButton.clicked.connect(self.classify)

        btn3 = getBtn(SUCCESS, "图像自动分类", self)
        btn3.clicked.connect(lambda : eventSystem.dispatch("changeTab", "imageCluster"))

        self.submitButton = submitButton
        return [
            submitButton,
            getBtn(INFO, "文本自动分类", self),
            getBtn(SUCCESS, "图像归类整理", self),
            btn3,
        ]
    def reset(self):
        self.searching = False
        self.worker = None
        self.submitButton.setText("重新分类")
    def classify(self):
        if self.searching:
            eventSystem.dispatch("stopSearch")
            self.worker.quit()
            self.worker.wait()
            self.reset()
        else:
            self.searching = True
            self.submitButton.setText("停止分类")
            eventSystem.dispatch("triggerResultPanel")
            self.worker = self._classify(self.getForm())
            self.worker.finishedTrigger.connect(self.reset)
    def _classify(self, rawData):
        worker = TextClusterThread()
        worker.initialize(rawData["classifyDirs"],rawData["cluster_n"], ["updatedTime","accessTime"])
        worker.start()
        worker.finishedTrigger.connect(lambda results: eventSystem.dispatch("finishTextCluster", results))
        self.worker = worker
        return worker
