from PyQt5.QtWidgets import QLineEdit, QLabel

from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from GUI.public.FormItem import FormItem
from core.SimilarImageSearchThread import SimilarImageSearchThread
from GUI.public.functions import getBtn, PRIMARY, INFO


class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.initUI("相似图像搜索",topMargin=80, bottomMargin=160)
    def createFieldGroup(self):
        self.createGroup(self.createRootDirctoryChoose, "搜索文件", 'compareObj',None, "file")
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'searchRoot')
        self.createGroup(self.createSimilarScore, "相似度", 'similarScore')
        self.createGroup(self.createQuantity, "搜索数量", 'quantity')
    def createSimilarScore(self):
        edit = QLineEdit(self)
        edit.setText("60")
        return (
            FormItem(edit, getVal=edit.text,col=2),
            FormItem(QLabel("%", self), col=1),
            FormItem(QLabel(self), col=3)
        )
    def createQuantity(self):
        edit = QLineEdit(self)
        edit.setText("10")
        return (
            FormItem(edit, getVal=edit.text, col=2),
            FormItem(QLabel("张", self), col=1),
            FormItem(QLabel(self), col=3)
        )
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
        workThread.initialize(data["compareObj"], data["searchRoot"], int(data["similarScore"]), int(data["quantity"]))
        workThread.start()
        workThread.finishedTrigger.connect(lambda results: eventSystem.dispatch("finishedSimilarImageSearch", results))
        self.workThread = workThread