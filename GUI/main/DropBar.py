from PyQt5.QtWidgets import QLabel
from GUI.main.EventSystem import eventSystem
class DropBar(QLabel):
    def __init__(self, parent, onForm=False):
        super().__init__(parent)
        self.onForm = onForm
        self.setObjectName("dropBar")
        self.setBackGrounImage()
    def setBackGrounImage(self):
        if self.onForm:
            self.setStyleSheet("""
            background-image: url(images/dropBar.png);
    background-position: left center;
    background-origin: content;
    background-repeat: none;
            """)
        else:
            self.setStyleSheet("""
            background-image: url(images/dropBarReverse.png);
    background-position: left center;
    background-origin: content;
    background-repeat: none;
            """)
    def mousePressEvent (self,  event):
        if self.onForm:
            self.setStatus(not self.onForm)
            eventSystem.dispatch("triggerResultPanel")
        else:
            self.setStatus(not self.onForm)
            eventSystem.dispatch("triggerFormPanel")

    def setStatus(self, isOn):
        if isOn:
            self.onForm = True
            self.setObjectName("dropBarOnForm")

        else:
            self.onForm = False
            self.setObjectName("dropBarOnResult")
        self.setBackGrounImage()
