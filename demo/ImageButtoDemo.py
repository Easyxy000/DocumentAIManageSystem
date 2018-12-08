from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from functions import config
class ImageButton(QPushButton):
    RESOURCE_DAR = config('config.resourceDir')
    def __init__(self, text, background, parent):
        super().__init__(text, parent)
        img = QIcon("{0}/{1}".format(ImageButton.RESOURCE_DAR, background))
        self.setIcon(img)
        self.setIconSize(self.size())