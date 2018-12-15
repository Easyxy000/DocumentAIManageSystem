from PyQt5.QtWidgets import QLineEdit

from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from GUI.public.FormItem import FormItem
from core.TextClusterThread import TextClusterThread
from GUI.public.functions import getBtn, PRIMARY, INFO, SUCCESS


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
        submitButton = getBtn(PRIMARY, "开始自动分类", self)
        submitButton.clicked.connect(self.classify)

        textClassifyBtn = getBtn(INFO, "文本自动归类", self)
        textClassifyBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "textClassify"))

        imageClassifyBtn = getBtn(INFO, "图像自动分类", self)
        imageClassifyBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "imageClassify"))

        imageClusterBtn = getBtn(INFO, "图像自动归类", self)
        imageClusterBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "imageCluster"))
        self.submitButton = submitButton
        return [
            submitButton,
            textClassifyBtn,
            imageClassifyBtn,
            imageClusterBtn
        ]
    def reset(self):
        self.searching = False
        self.worker = None
        self.submitButton.setText("重新分类")
    def classify(self):
        if self.searching:
            eventSystem.dispatch("stopTextCluster")
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
        eventSystem.dispatch("setTextCluster", rawData["cluster_n"])
        return worker
