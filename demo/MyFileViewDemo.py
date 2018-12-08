#!/usr/bin/env python3

import sys
from PyQt5.QtCore import QFile, QTimer, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QSplitter, QTableView, QTreeView, QVBoxLayout,
                             QWidget, QItemDelegate)
from demo.MyFileTableDemo import FileTableModel
MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False
from demo.Field import Field
from functions import timestampConvertToString, fileSizeConvertToFitUnit
class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('读'),
                self.parent(),
                # clicked=self.parent().cellButtonClicked
            )
            button_write = QPushButton(
                self.tr('写'),
                self.parent(),
                # clicked=self.parent().cellButtonClicked
            )
            button_read.index = [index.row(), index.column()]
            button_write.index = [index.row(), index.column()]
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.addWidget(button_write)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(
                index,
                widget
            )
class MainForm(QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        fields = [
            Field("count", "个数", editable=True),
            Field("fileName", "文件名", editable=True),
            Field("fileSize", "文件大小", formatMethod=fileSizeConvertToFitUnit),
            Field("createdTime", "创建时间",  formatMethod=timestampConvertToString),
            Field("updatedTime", "修改时间", formatMethod=timestampConvertToString),
            Field("accessTime", "最近一次访问时间", formatMethod=timestampConvertToString),
            Field("path", "所属目录")
        ]
        self.model = FileTableModel(fields)
        tableLabel = QLabel("Table &1")
        self.tableView = QTreeView()
        tableLabel.setBuddy(self.tableView)
        self.tableView.setModel(self.model)

        self.tableView.setItemDelegateForColumn(0, MyButtonDelegate(self.tableView))
        splitter = QSplitter(Qt.Horizontal)

        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel)
        vbox.addWidget(self.tableView)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)

        button = QPushButton("添加一行")
        def addLine():
            self.model.insertRows(self.model.rowCount(), {"fileSize": 386958,
            "createdTime": 1543762154.0,
            "updatedTime": 1543762149.0,
            "accessTime": 1543762149.0,
            "fileName": "非你莫属.jpg",
             "path" : "﻿/Users/xushaojun/Documents/吉他谱"},)
        button.clicked.connect(addLine)


        layout = QVBoxLayout()

        layout.addWidget(button)
        layout.addWidget(splitter)
        self.setLayout(layout)

        # header = self.tableView.horizontalHeader()
        # self.tableView.he
        header = self.tableView.header()
        header.sectionClicked[int].connect(self.sortTable)

        self.setWindowTitle("Ships (model)")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):

        files = [
            {"count" : 1,
             "fileSize": 386958,
            "createdTime": 1543762154.0,
            "updatedTime": 1543762149.0,
            "accessTime": 1543762149.0,
            "fileName": "你一定要幸福.jpg",
             "path" : "﻿/Users/xushaojun/Documents/吉他谱"},
            {"count" :1,
             "fileSize": 586490,
            "createdTime": 1528033738.0,
            "updatedTime": 1528033726.0,
            "accessTime": 1528033726.0,
            "fileName": "说你也一样爱着我.png",
             "path": "﻿/Users/xushaojun/Documents/吉他谱/张栋梁"}
        ]
        for file in files:
            self.model.files.append(file)
        self.model.endResetModel()
        self.model.dirty = False
        self.model.sortByField("fileName")
        self.resizeColumns()
    def resizeColumns(self):
        for tableView in (self.tableView, ):
            for column in range(6):
                tableView.resizeColumnToContents(column)
    def sortTable(self, section):
        print("sorted")
        self.model.sortByField(section)
        self.resizeColumns()




app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()