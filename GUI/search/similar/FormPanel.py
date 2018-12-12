from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from core.SimilarImageSearchThread import SimilarImageSearchThread
from functions import getBtn, PRIMARY, INFO


class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.initUI("相似图像搜索",topMargin=160, bottomMargin=160)
    def createFieldGroup(self):
        self.createGroup(self.createRootDirctoryChoose, "搜索文件", 'compareObj',None, "file")
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'searchRoot')
    def getBtns(self):
        searchBtn = getBtn(PRIMARY, "开始搜索", self)
        normalFileSearchBtn = getBtn(INFO, "一般文件搜索", self)

        searchBtn.clicked.connect(self.search)
        normalFileSearchBtn.clicked.connect(lambda: eventSystem.dispatch("changeTab", "normalSearch"))

        return (searchBtn, normalFileSearchBtn)
    def search(self):
        eventSystem.dispatch("triggerResultPanel")
        workThread = SimilarImageSearchThread()
        data = self.getForm()
        workThread.initialize(data["compareObj"], data["searchRoot"])
        workThread.start()
        workThread.finishedTrigger.connect(lambda results: eventSystem.dispatch("finishedSimilarImageSearch", results))
        self.workThread = workThread