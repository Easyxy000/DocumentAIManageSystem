from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt, QRect
from functions import config
from GUI.EventSystem import eventSystem
class MenuItem(QLabel):
    def __init__(self, parent, name, id):
        super().__init__(name, parent)
        self.setAlignment(Qt.AlignCenter)
        self.id = id
    def enterEvent (self, event):
        # print("enter " + self.id)
        pass
    def leaveEvent(self, event):
        # print("leave " + self.id)
        pass
    def mousePressEvent (self,  event):
        eventSystem.dispatch("changeTab", self.id)
class MainMenu(QWidget):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.resize(*size)
        self.initUI(size)
    def initUI(self, size):


        menus = (
            ('文件搜索', 'search'),
            ('重复文件检测', 'check'),
            ('文件整理', 'format'),
            ('系统设置', 'setting'),
        )

        w, h = size[0], size[1] / len(menus)
        y = 0
        for menu in menus:
            item = MenuItem(self, *menu)
            item.resize(w, h)
            item.setStyleSheet(config("gui.menuItemStyle").format(menu[1]))
            item.setObjectName("menuItem")
            item.setFrameRect(QRect(0, 100, w, 30))
            item.move(0, y)
            y += h