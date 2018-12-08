#!/usr/bin/env python3

import sys
from PyQt5.QtCore import QFile, QTimer, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QSplitter, QTableView, QTreeView, QVBoxLayout,
                             QWidget, QItemDelegate)
from demo.MyFileTableDemo import FileTableModel
from demo.myView.mainForm import MainForm

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()