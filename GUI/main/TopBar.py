from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from GUI.public.functions import config
class TopBar(QWidget):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.resize(*size)
        lineW, btnW = config("gui.topBarSearchLineWidth"), config("gui.topBarSearchBtnWidth")
        H = config("gui.topBarSearchHeight")
        x = int(size[0] * config("gui.formWeightPercentage") - lineW - btnW)
        y = (size[1] - H) // 4

        searchEdit = QLabel(self)
        searchEdit.setObjectName("topBarSearchLine")
        searchEdit.resize(lineW, H)
        searchEdit.move(x, y)
        x += lineW

        btn = QPushButton(self)
        btn.setObjectName("topBarSearchBtn")
        btn.resize(btnW, H)
        btn.move(x, y)