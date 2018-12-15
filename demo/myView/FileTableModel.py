#!/usr/bin/env python3

import os
import shutil

from PyQt5.QtCore import (QAbstractTableModel, QModelIndex, QVariant, Qt, pyqtSignal)
from PyQt5.QtWidgets import QFileDialog

from core.Field import Field
from GUI.public.functions import openFile

FILENAME, DIR, FILE_SIZE, CREATED_DATE, UPDATED_DATE, ACCESS_DATE = range(6)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1

class FileTableModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex,QModelIndex)
    def __init__(self, fields, specialColumn=None, pageSize=10):
        super(FileTableModel, self).__init__()
        self.tableView = None
        # files
        self.files = []
        self.fields = fields
        self.fieldIDMap = dict([(field.id, field) for field in fields])
        self.checkList = []

        # specialColumn
        self.specialColumn = specialColumn
        self.specialColumnCount = len(specialColumn) if type(specialColumn) == list else None
    def sortByField(self, idOrRank):
        if idOrRank == 0:
            return
        idOrRank -= self.specialColumnCount + 1
        if idOrRank < self.specialColumnCount: return
        field : Field = self.fields[idOrRank] if type(idOrRank) == int else self.fieldIDMap[idOrRank]
        if not field.comparable:
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
                return self.getFormatVal(file, col - self.specialColumnCount)
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
        if field.delegateClass is not None:
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
                elif section <= self.specialColumnCount:
                    return self.specialColumn[section - 1]
                else:
                    return self.fields[section - self.specialColumnCount].name
    def rowCount(self, index=QModelIndex()):
        return len(self.files)
    def columnCount(self, index=QModelIndex()):
        return len(self.fields) + self.specialColumnCount
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
        self.dirty = True
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
        if fname == "": return
        for row in self.getCheckedIds():
            file = self.files[row]
            fileName = file["fileName"]
            shutil.move(self.getCompletePath(row), os.path.join(fname, fileName))
            file["path"] = fname
    def deleteChecked(self):
        for row in self.getCheckedIds():
            p = self.getCompletePath(row)
            if os.path.isdir(p):
                os.rmdir(p)
            else:
                os.remove(p)
            print("delete {0}".format(p))
