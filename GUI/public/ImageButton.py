from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from functions import config
class ImageButton(QPushButton):
    RESOURCE_DAR = config('config.resourceDir')
    def __init__(self, text, parent, background="button.png"):
        super().__init__(text, parent)
        self.setStyleSheet('QPushButton{{border-width:4px;border-image:url({0}/{1})  4 4 4 4 stretch stretch; padding:0; margin:0;border:0;}}'.format(ImageButton.RESOURCE_DAR, background))