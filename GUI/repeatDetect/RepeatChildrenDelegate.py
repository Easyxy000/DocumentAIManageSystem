from PyQt5.Qt import Qt, QSize

from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout

from functions import getBtn, PRIMARY


class RepeatChildrenDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(RepeatChildrenDelegate, self).__init__(parent)
        self.sizeCache = QSize(100, 40)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            widget = QWidget()

            btn = QPushButton("查看重复项", widget)
            btn.clicked.connect(lambda : self.printChildren(index.row()))
            btn.setObjectName("tableViewPrimaryBtn")

            layout = QHBoxLayout()
            layout.addWidget(btn)

            widget.setLayout(layout)
            widget.setObjectName("QTableViewDelegate")
            self.parent().setIndexWidget(
                index,
                widget
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):

        return self.sizeCache
    def printChildren(self, row):
        data = self.parent().model.rowData(row)
        for item in data["children"]:
            print(item)