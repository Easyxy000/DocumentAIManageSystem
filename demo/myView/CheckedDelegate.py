from PyQt5.Qt import Qt, QSize, QCheckBox

from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout


class CheckedDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(CheckedDelegate, self).__init__(parent)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            cb = QCheckBox(self.parent())
            cb.stateChanged.connect(lambda state: self.parent().checkItem(index.row(), state))
            self.parent().setIndexWidget(
                index,
                cb
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        size: QSize = QItemDelegate.sizeHint(self, option, index)
        size.setWidth(100)
        return size