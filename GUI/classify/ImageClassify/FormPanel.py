import os

from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from core.ImageClassifyThread import ImageClassifyThread
from GUI.public.functions import getBtn, PRIMARY, INFO


class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.form = {}
        self.checkedType = {}
        self.searcher = None
        self.searching = False
        self.initUI("图像自动归类",topMargin=120, bottomMargin=200)
        eventSystem.listen("stopSearch", self.stopSearch, self)
    def createFieldGroup(self):
        self.createGroup(self.createRootDirctoryChoose, "已归类文件夹", 'classifyDirs')
        self.createGroup(self.createRootDirctoryChoose, "散乱文件所在文件夹", 'predictDir')
    def stopSearch(self):
        if self.worker is not None:
            self.worker.quit()
            self.worker.wait()
    def getBtns(self):
        submitButton = getBtn(PRIMARY, "开始归类整理", self)
        submitButton.clicked.connect(self.classify)

        textClassifyBtn = getBtn(INFO, "文本自动归类", self)
        textClassifyBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "textClassify"))

        textClusterBtn = getBtn(INFO, "文本自动分类", self)
        textClusterBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "textCluster"))

        imageClusterBtn = getBtn(INFO, "图像自动归类", self)
        imageClusterBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "imageCluster"))

        self.submitButton = submitButton
        return [
            submitButton,
            textClassifyBtn,
            textClusterBtn,
            imageClusterBtn,
        ]
    def reset(self):
        self.searching = False
        self.worker = None
        self.submitButton.setText("重新分类")
    def classify(self):
        if self.searching:
            eventSystem.dispatch("stopImageClassify")
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
        root = rawData["classifyDirs"]
        worker = ImageClassifyThread()
        worker.initialize(root,rawData["predictDir"], ["updatedTime","accessTime"])
        worker.start()
        classNames = []
        classDirs = []
        for item in os.listdir(root):
            if item[0] == ".": continue
            p = os.path.join(root, item)
            if not os.path.isdir(p): continue
            classNames.append(item)
            classDirs.append(p)
        eventSystem.dispatch("setImageClass", classNames, classDirs)
        worker.finishedTrigger.connect(lambda results: eventSystem.dispatch("finishImageClassify", results))
        self.worker = worker
        print("classify!")
        return worker
