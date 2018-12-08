from PyQt5.QtWidgets import QWidget, QLabel

from GUI.EventSystem import eventSystem


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
    def enterEvent (self, event):
        # print("enter " + self.id)
        pass
    def leaveEvent(self, event):
        # print("leave " + self.id)
        pass
    def mousePressEvent (self,  event):
        if self.onForm:
            self.setStatus(not self.onForm)
            eventSystem.dispatch("triggerResult")
        else:
            self.setStatus(not self.onForm)
            eventSystem.dispatch("triggerForm")

    def setStatus(self, isOn):
        if isOn:
            self.onForm = True
            self.setObjectName("dropBarOnForm")

        else:
            self.onForm = False
            self.setObjectName("dropBarOnResult")
        self.setBackGrounImage()
