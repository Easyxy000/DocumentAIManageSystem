# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from GUI.MainWindow import MainWindow
from configs.GUI import GUI_SETTINGS
app = QApplication(sys.argv)
ex = MainWindow(GUI_SETTINGS['title'], GUI_SETTINGS['size'])
sys.exit(app.exec_())