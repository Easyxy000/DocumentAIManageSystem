# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from GUI.MainWindow import MainWindow
from configs.GUI import GUI_CONFIGS
app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())