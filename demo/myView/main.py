#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (QApplication)
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