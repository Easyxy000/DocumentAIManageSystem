from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QPushButton
from GUI.main.MainContent import MainContent
from GUI.main.BottomBar import BottomBar
from GUI.public.functions import config
from GUI.main.MainMenu import MainMenu
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化窗口
        windowSize =  config('gui.windowSize')
        self.resize(*windowSize)
        self.center()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(config('gui.windowTitle'))

        # 初始化是否最大化
        self.isNormal = True



        leftSideW = int(windowSize[0] * config('gui.leftSidePercentage'))


        logoRectH = int(config('gui.logoRectHeightPercentage') * windowSize[1])
        logoRect = QLabel(self)
        logoRect.setObjectName("logoBox")
        logoRect.resize(leftSideW, logoRectH)


        menu = MainMenu(self, (leftSideW, windowSize[1] - logoRectH))
        menu.move(0, logoRectH)


        mainW = windowSize[0] - leftSideW

        x = leftSideW
        y = 0

        topBorderH = config('gui.topBorderHeight')
        topBorder = self.createTopBorder(mainW, topBorderH)
        topBorder.move(leftSideW, 0)
        y += topBorderH


        mainContentH =  config('gui.mainContentHeight')
        mainContent = MainContent(self,(mainW, mainContentH), config('gui.defaultTab'))
        mainContent.move(x, y)
        y += mainContentH


        bottomBar = BottomBar(self, (mainW, config("gui.bottomBarHeight")))
        bottomBar.move(x, y)
        bottomBar.setObjectName("bottomBar")
        # vbox = QVBoxLayout()
        # self.setLayout(vbox)
        #
        # vbox.addWidget(TopBar(self))
        # vbox.addWidget(MainContent(self,'index'))
        # vbox.addWidget(BottomBar(self))
        self.setObjectName("mainWindow")
        self.setStyleSheet(config('globalStyleSheet'))
        self.show()
    def createTopBorder(self, w, h):

        topBorder = QLabel(self)
        topBorder.resize(w, h)

        btnSize = config("gui.topBorderBtnSize")

        narrowBtn = QPushButton(topBorder)
        narrowBtn.setObjectName("topBorderNarrowBtn")
        narrowBtn.clicked.connect(self.showMinimized)


        amplificationBtn = QPushButton(topBorder)
        amplificationBtn.setObjectName("topBorderAmplificationBtn")
        amplificationBtn.clicked.connect(self.amplification)


        closeBtn = QPushButton(topBorder)
        closeBtn.setObjectName("topBorderCloseBtn")
        closeBtn.clicked.connect(self.close)

        btns = (narrowBtn, amplificationBtn, closeBtn)

        margin = config("gui.topBorderBtnMargin")
        marginRight = config("gui.topBorderBtnMarginRight")
        x = w - len(btns) * (btnSize[0] + margin) + margin - marginRight
        y = config("gui.topBorderBtnMarginTop")
        for btn in btns:
            btn.move(x, y)
            x += margin + btnSize[0]
        return topBorder
    def amplification(self):
        if self.isNormal:
            self.showMaximized()
        else:
            self.showNormal()
        self.isNormal = not self.isNormal
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())