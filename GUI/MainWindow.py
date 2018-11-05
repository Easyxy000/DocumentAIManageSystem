from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from configs.GUI import GUI_SETTINGS
class MainWindow(QWidget):

    def __init__(self, title, size=(250, 250)):
        super().__init__()
        self.resize(*size)
        self.center()
        self.setWindowTitle(title)
        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())