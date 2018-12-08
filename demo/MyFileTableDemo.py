#!/usr/bin/env python3

import platform
from PyQt5.QtCore import (QAbstractTableModel, QDataStream, QFile,
                          QIODevice, QModelIndex, QVariant, Qt, pyqtSignal, QAbstractItemModel)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

from functions import fileSizeConvertToFitUnit, timestampConvertToString
FILENAME, DIR, FILE_SIZE, CREATED_DATE, UPDATED_DATE, ACCESS_DATE = range(6)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1

class FileTableModel(QAbstractTableModel):
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
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable)
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

