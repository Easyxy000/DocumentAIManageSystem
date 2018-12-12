from PyQt5.Qt import Qt, QSize

from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout


class ActionDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ActionDelegate, self).__init__(parent)
        self.sizeCache = None
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            widget = QWidget()

            btn = QPushButton("查看重复项",widget)
            btn.clicked.connect(lambda : self.parent().model.rowData(index.row()))
            btn.setObjectName("tableViewOpenBtn")
            widget.setObjectName("QTableViewDelegate")
            self.parent().setIndexWidget(
                index,
                widget
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        if self.sizeCache is None:
            size: QSize = QItemDelegate.sizeHint(self, option, index)
            size.setWidth(100)
            self.sizeCache = size
        return self.sizeCache