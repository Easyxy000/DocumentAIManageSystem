#!/usr/bin/env python3
import os
import shutil
from PyQt5.QtCore import (QAbstractTableModel, QModelIndex,QVariant, Qt,pyqtSignal)
from PyQt5.QtWidgets import QFileDialog
from core.Field import Field
from GUI.public.functions import openFile, questionDialog, infoDialog


class FileTableModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex,QModelIndex)
    def __init__(self, fields):
        super(FileTableModel, self).__init__()
        self.tableView = None
        self.files = []
        self.fields = fields
        self.fieldIDMap = dict([(field.id, field) for field in fields])
        self.checkList = []
    def sortByField(self, idOrRank):
        field : Field = self.fields[idOrRank] if type(idOrRank) == int else self.fieldIDMap[idOrRank]
        if not field.hasValue or not field.comparable:
            return
        self.beginResetModel()
        self.files = sorted(self.files, key=lambda x : (x[field.id],), reverse=field.reverse)
        field.reverse = not field.reverse
        self.endResetModel()
    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return Qt.ItemIsEnabled
    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.files))):
            return QVariant()
        row, col = index.row(), index.column()
        file = self.files[row]
        if role == Qt.DisplayRole:
            if col == 0:
                return ""
            else:
                return self.getFormatVal(file, col - 1)
        elif role == Qt.CheckStateRole:
            if col == 0:
                return Qt.Checked if self.checkList[row] == True else Qt.Unchecked
            elif col == 1:
                return None
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        return QVariant()
    def getFormatVal(self,file, col):
        field = self.fields[col]
        if not field.hasValue:
            return None
        val = file[field.id]
        if field.formatMethod is None:
            return val
        else:
            return field.formatMethod(val)
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return ""
                else:
                    return self.fields[section - 1].name
    def rowCount(self, index=QModelIndex()):
        return len(self.files)
    def columnCount(self, index=QModelIndex()):
        return len(self.fields) + 1
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole and index.column() == 0:
            self.checkList[index.row()] = True if value == Qt.Checked else False
            return True
    def insertRow(self, item, position=None, index=QModelIndex()):
        position = self.rowCount()
        self.beginInsertRows(QModelIndex(), position, position)
        self.files.insert(position + 1, item)
        self.checkList.insert(position + 1, False)
        self.endInsertRows()
        return True
    def headerClick(self, isOn):
        self.beginResetModel()
        if isOn:
            self.checkList = [True] * self.rowCount()
        else:
            self.checkList = [False] * self.rowCount()
        self.endResetModel()
    def load(self, files):
        self.files = files
        self.checkList = [False] * len(files)
        self.beginResetModel()
        self.endResetModel()
    def getCompletePath(self, row):
        file = self.files[row]
        return os.path.join(file["path"], file["fileName"])
    def open(self, row):
        openFile(self.getCompletePath(row))
    def getCheckedIds(self):
        ids = []
        for i in range(len(self.checkList)):
            if self.checkList[i] == True:
                ids.append(i)
        return ids

    def openChecked(self):
        for row in self.getCheckedIds():
            self.open(row)
    def moveChecked(self):
        fname = QFileDialog.getExistingDirectory(self.tableView, 'Open file', '/home')
        self.beginResetModel()
        if fname == "": return
        ids = self.getCheckedIds()
        if len(ids) <= 0:
            infoDialog("请选择文件", self.tableView)
            return
        f, l = self.files[ids[0]]["fileName"],  len(ids)
        if not questionDialog("您确认要\"{0}\"等{1}项文件移动到文件夹\"{2}\"".format(f, l, fname), self.tableView):
            return
        fileNameCount = dict()
        for row in ids:
            file = self.files[row]
            fileName = file["fileName"]
            if fileName in fileNameCount:
                s = fileName.find(".")
                if s == -1:
                    fileName = fileName + str(fileNameCount[fileName] + 1)
                else:
                    fileName = fileName[:s] + str(fileNameCount[fileName] + 1) + fileName[s:]
            else:
                fileNameCount[fileName] = 1
            shutil.move(self.getCompletePath(row), os.path.join(fname, fileName))
            file["path"] = fname
        infoDialog("您已成功将\"{0}\"等{1}项文件移动到文件夹\"{2}\"".format(f, l, fname), self.tableView)
        self.endResetModel()

    def deleteChecked(self):
        self.beginResetModel()
        ids = self.getCheckedIds()
        if len(ids) <= 0:
            infoDialog("请选择文件", self)
            return
        f, l = self.files[ids[0]]["fileName"],  len(ids)
        if not questionDialog("您确认要删除\"{0}\"等{1}项文件".format(f, l), self.tableView):
            return
        for row in ids:
            p = self.getCompletePath(row)
            if os.path.isdir(p):
                os.rmdir(p)
            else:
                os.remove(p)
            print("delete {0}".format(p))
            self.removeRow(row)
            self.files.remove(self.files[row])
        self.endResetModel()
        infoDialog("您已成功删除\"{0}\"等{1}项文件".format(f, l), self.tableView)
    def rowData(self, row):
        return self.files[row]