import sys
from PyQt5.QtWidgets import QApplication, QWidget


class ViewTestWindow(QWidget):
    def __init__(self):
        super(ViewTestWindow, self).__init__()
        self.setMinimumSize(800, 600)

app = QApplication(sys.argv)
window = ViewTestWindow()
window.show()
app.exec_()