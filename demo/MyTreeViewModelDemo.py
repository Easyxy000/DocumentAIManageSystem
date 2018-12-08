#!/usr/bin/env python3

import platform

import sys
from PyQt5.QtCore import (QModelIndex, QVariant, Qt, pyqtSignal, QAbstractItemModel, QTimer)
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QSplitter, QTreeView, QLabel, QDialog

from core.Field import Field
from functions import fileSizeConvertToFitUnit, timestampConvertToString

FILENAME, DIR, FILE_SIZE, CREATED_DATE, UPDATED_DATE, ACCESS_DATE = range(6)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1

class FileTableModel(QAbstractItemModel):
    dataChanged = pyqtSignal(QModelIndex,QModelIndex)
    def __init__(self, fields):
        super(FileTableModel, self).__init__()
        self.dirty = False
        self.files = []
        self.fields = fields
        self.fieldIDMap = dict([(field.id, field) for field in fields])
    def sortByField(self, idOrRank):
        field = self.fields[idOrRank] if type(idOrRank) == int else self.fieldIDMap[idOrRank]
        self.beginResetModel()
        self.files = sorted(self.files, key=lambda x : (x[field.id],), reverse=field.reverse)
        field.reverse = not field.reverse
        self.endResetModel()
    # def flags(self, index):
    #     if not index.isValid():
    #         return Qt.ItemIsEnabled
    #     return Qt.ItemFlags(
    #             QAbstractItemModel.flags(self, index)|
    #             Qt.ItemIsEditable)
    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.files))):
            return QVariant()
        file = self.files[index.row()]
        if role == Qt.DisplayRole:
          return self.getFormatVal(file, index)
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        return QVariant()
    def getFormatVal(self,file, index):
        field = self.fields[index.column()]
        val = file[field.id]
        if field.formatMethod is None:
            return val
        else:
            return field.formatMethod(val)
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(self.fields[section].name)
        return QVariant(int(section + 1))
    def rowCount(self, index=QModelIndex()):
        return len(self.files)
    def columnCount(self, index=QModelIndex()):
        return len(self.fields)
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.files):
            #self.beginResetModel()
            file = self.files[index.row()]
            field = self.fields[index.column()]
            if field.editable == False: return False
            file[field.id] = str(value)
            self.dirty = True
            self.dataChanged[QModelIndex,QModelIndex].emit(index,index)
            #self.endResetModel()
            return True
        return False
    def insertRows(self, position, data, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.files.insert(position + row,
                              data)
        self.endInsertRows()
        self.dirty = True
        return True
    def index(self, row, column, parent=QModelIndex()):
        # assert self.root
        # branch = self.nodeFromIndex(parent)
        # assert branch is not None
        return self.createIndex(row, column,
                                self.files[parent.row()]["child"][row])


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        fields = [
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
            {"fileSize": 386958,
            "createdTime": 1543762154.0,
            "updatedTime": 1543762149.0,
            "accessTime": 1543762149.0,
            "fileName": "你一定要幸福.jpg",
             "path" : "﻿/Users/xushaojun/Documents/吉他谱",
             "child" : [
                 {"fileSize": 586490,
                  "createdTime": 1528033738.0,
                  "updatedTime": 1528033726.0,
                  "accessTime": 1528033726.0,
                  "fileName": "王子.png",
                  "path": "﻿/Users/xushaojun/Documents/吉他谱/张栋梁"},
                 {"fileSize": 586490,
                  "createdTime": 1528033738.0,
                  "updatedTime": 1528033726.0,
                  "accessTime": 1528033726.0,
                  "fileName": "小乌龟.png",
                  "path": "﻿/Users/xushaojun/Documents/吉他谱/张栋梁"}
             ]},
            {"fileSize": 586490,
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