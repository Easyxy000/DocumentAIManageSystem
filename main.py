# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from GUI.main.MainWindow import MainWindow
app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())