from PyQt5.QtWidgets import QLabel

from GUI.DropBar import DropBar
from GUI.EventSystem import eventSystem
from functions import config
class MainContentTab(QLabel):
    def __init__(self, parent,size, id):
        super().__init__(parent)
        self.resize(size)
        self.id = id
        eventSystem.listen("triggerForm", self.triggerForm, self)
        eventSystem.listen("triggerResult", self.triggerResult, self)
    def initUI(self):
        pass
    def createFormAndResult(self, FormConstructor, ResultConstructor, mainWeightRecentgage = 0.6):
        size = self.size()
        w, h = size.width(), size.height()

        dropW = config("gui.dropBarWidth")
        dropLeftMargin = config("gui.dropBarLeftMargin")

        formW = int(w * config("gui.formWeightPercentage"))
        form = FormConstructor(self)
        form.resize(formW, h)
        form.show()

        resultSize = (w - dropW - dropLeftMargin, h)
        result = ResultConstructor(self, resultSize)
        result.resize(*resultSize)
        result.hide()

        dropBar = DropBar(self, onForm=True)
        dropBar.resize(dropW, h)
        dropBar.move(formW, 0)
        dropBar.show()

        self.formPanel = form
        self.resultPanel = result
        self.dropBar = dropBar
    def triggerForm(self):
        self.formPanel.show()
        self.resultPanel.hide()
        self.dropBar.move(self.formPanel.size().width() + config("gui.dropBarLeftMargin"), 0)
        self.dropBar.setStatus(True)
    def triggerResult(self):
        self.resultPanel.show()
        self.formPanel.hide()
        self.dropBar.move(self.resultPanel.size().width() + config("gui.dropBarLeftMargin"), 0)
        self.dropBar.setStatus(False)
