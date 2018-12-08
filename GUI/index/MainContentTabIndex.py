from GUI.MainContentTab import MainContentTab
from PyQt5.QtWidgets import QLabel
from PyQt5.Qt import Qt
class MainContentTabIndex(MainContentTab):
    def __init__(self, parent):
        super().__init__(parent, 'index')
        self.createFormAndResult(QLabel(self), QLabel(self))
    def initMain(self, main):
        pass
    def initSide(self, side):
        pass