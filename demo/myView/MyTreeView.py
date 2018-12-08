from PyQt5 import QtCore

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableView, QFrame, QAbstractItemView

from demo.myView.CheckBoxHeader import CheckBoxHeader


class MyTreeView(QTableView):
    def __init__(self, model,fields):
        super(MyTreeView, self).__init__()
        model.tableView = self
        self.fields = fields
        self.setModel(model)
        self.model = model
        self.setFrameShape(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = CheckBoxHeader()
        self.setHorizontalHeader(header)
    # def sizeHintForColumn(self, column: int):
    #     getSizeHin = self.fields[column].getSizeHint
    #     return getSizeHin() if getSizeHin is not None else super(MyTreeView, self).sizeHintForColumn(column)