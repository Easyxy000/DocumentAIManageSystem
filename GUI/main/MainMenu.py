from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.Qt import Qt, QRect
from GUI.public.functions import config
from GUI.main.EventSystem import eventSystem
class MenuItem(QLabel):
    def __init__(self, parent, name, id, defaultTab=None):
        super().__init__(name, parent)
        self.setAlignment(Qt.AlignCenter)
        self.id = id
        self.selected = False
        if id == config('gui.defaultTab'):
            self.selected = True
            self.setSelected(True)
        self.tabId = id if defaultTab is None else defaultTab
    def enterEvent (self, event):
        self.setSelected(True)
    def leaveEvent(self, event):
        if not self.selected:
            self.setSelected(False)
    def setSelected(self, selected):
        if selected:
            self.setStyleSheet("""
                   background-color:#8095ba;
                   color:#abb6cb;
               """)
            self.setStyleSheet(config("gui.menuItemFocusStyle").format(self.id))
        else:
            self.setStyleSheet("""
                  background-color:#96add4;
                  color:#abb6cb;
              """)
            self.setStyleSheet(config("gui.menuItemStyle").format(self.id))
    def mousePressEvent (self,  event):
        eventSystem.dispatch("changeTab", self.tabId)
class MainMenu(QWidget):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.resize(*size)
        self.initUI(size)
    def initUI(self, size):
        menuData = (
            ('文件搜索', 'search',"normalSearch"),
            ('重复文件检测', 'repeatDetect'),
            ('文件整理', 'classify', 'textClassify'),
            ('系统设置', 'setting'),
        )
        menus = []

        w, h = size[0], size[1] / len(menuData)
        y = 0
        for menu in menuData:
            item = MenuItem(self, *menu)
            item.resize(w, h)
            item.setStyleSheet(config("gui.menuItemStyle").format(menu[1]))
            item.setObjectName("menuItem")
            item.setFrameRect(QRect(0, 100, w, 30))
            item.move(0, y)
            y += h
            menus.append(item)

        self.menus = menus
        eventSystem.listen("selectedMenu", self.selectedMenu, self)
    def selectedMenu(self, id):
        for menu in self.menus:
            if id == menu.id:
                menu.selected = True
                menu.setSelected(True)
            else:
                menu.selected = False
                menu.setSelected(False)
