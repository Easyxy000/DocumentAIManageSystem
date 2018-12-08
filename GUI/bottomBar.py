from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.Qt import Qt
from functions import config
class BottomBar(QLabel):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.resize(*size)

        leftW = int(size[0] * config("gui.formWeightPercentage"))
        bottomTitle = QLabel("@魔方管家",self)
        bottomTitle.resize(leftW, 30)
        bottomTitle.move(0, 10)
        bottomTitle.setAlignment(Qt.AlignCenter)
        bottomTitle.setObjectName("bottomTitle")

        bottomSmallTitle = QLabel("文件智能管理工具", self)
        bottomSmallTitle.resize(leftW, 20)
        bottomSmallTitle.move(0, 30)
        bottomSmallTitle.setAlignment(Qt.AlignCenter)
        bottomSmallTitle.setObjectName("bottomSmallTitle")

        checkUpdateSize = config("gui.checkUpdateSize")
        CW, CH = checkUpdateSize[0], checkUpdateSize[1]
        checkUpdate = QLabel( "检查更新",self)
        checkUpdate.setAlignment(Qt.AlignCenter)
        checkUpdate.resize(*checkUpdateSize)
        checkUpdate.move(leftW + int((size[0] - CW - leftW)/2), int((size[1] - CH)/2))
        checkUpdate.setObjectName("checkUpdate")

        # checkUpdate.resize(w - HMargin, h)
        # checkUpdate.setAlignment(Qt.AlignRight)
        self.show()
