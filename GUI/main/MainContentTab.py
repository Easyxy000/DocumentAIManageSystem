from PyQt5.QtWidgets import QLabel
from GUI.main.DropBar import DropBar
from GUI.main.EventSystem import eventSystem
from GUI.main.TopBar import TopBar
from GUI.public.functions import config
class MainContentTab(QLabel):
    def __init__(self, parent,size, id):
        super().__init__(parent)
        self.resize(size)
        self.id = id
        self.listenEvents()
    def listenEvents(self):
        # 监听事件
        eventSystem.listen("triggerFormPanel", self.triggerFormPanel, self)
        eventSystem.listen("triggerResultPanel", self.triggerResultPanel, self)
    def createFormAndResult(self, FormConstructor, ResultConstructor):
        # 获得尺寸
        size = self.size()
        w, h = size.width(), size.height()

        # 初始化拖动条尺寸
        dropW = config("gui.dropBarWidth")
        dropLeftMargin = config("gui.dropBarLeftMargin")

        # 创建头部搜索框
        topbarH = config('gui.topBarHeight')
        topbar = TopBar(self,(w, topbarH))
        topbar.show()

        # 创建表单面板
        formW = int(w * config("gui.formWeightPercentage"))
        formPanel = FormConstructor(self)
        formPanel.resize(formW, h - topbarH)
        formPanel.move(0, topbarH)
        formPanel.show()

        # 创建结果面板
        resultSize = (w - dropW - dropLeftMargin, h)
        resultPanel = ResultConstructor(self, resultSize)
        resultPanel.resize(*resultSize)
        resultPanel.hide()


        # 创建拖动条
        dropBar = DropBar(self, onForm=True)
        dropBar.resize(dropW, h - topbarH)
        dropBar.move(formW, topbarH)
        dropBar.show()

        # 赋予成员变量
        self.topBar = topbar
        self.formPanel = formPanel
        self.resultPanel = resultPanel
        self.dropBar = dropBar
        self.topbarH = topbarH
    def triggerFormPanel(self):
        self.topBar.hide()
        self.formPanel.show()
        self.resultPanel.hide()
        self.dropBar.move(
            self.formPanel.size().width() + config("gui.dropBarLeftMargin"),
            self.topbarH
        )
        self.dropBar.setStatus(True)

    def triggerResultPanel(self):
        self.topBar.show()
        self.resultPanel.show()
        self.formPanel.hide()
        self.dropBar.move(
            self.resultPanel.size().width() + config("gui.dropBarLeftMargin"),
            self.topbarH
        )
        self.dropBar.setStatus(False)
    def show(self):
        super().show()
        self.listenEvents()
    def hide(self):
        super().hide()
        eventSystem.removeAllListen(self)