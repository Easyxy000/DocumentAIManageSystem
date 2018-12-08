from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.Qt import Qt
from functions import config
class TopBar(QWidget):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.resize(*size)
        # topWeight = config('gui.windowSize')[0]
        # topHeiht = config('gui.topBarHeight')
        # mainMenuPercentage = config('gui.mainMenuPercentage')
        # top = QWidget(self)
        # top.resize(topWeight, topWeight)
        #
        #
        # mainMenuWeight = topWeight * mainMenuPercentage
        # mainMenu = MainMenu(top,(mainMenuWeight, topHeiht))
        # label = QLabel(top)
        # label.resize(topWeight * (1 - mainMenuPercentage), topHeiht)
        # label.setAlignment(Qt.AlignCenter)
        # label.setText("最骚的软件")
        # label.move(mainMenuWeight, 0)