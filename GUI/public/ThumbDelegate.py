from PyQt5.Qt import Qt, QSize, QPixmap

from PyQt5.QtWidgets import QItemDelegate, QLabel, QHBoxLayout
import  os

class ThumbDelegate(QItemDelegate):
    def __init__(self, parent, size):
        super(ThumbDelegate, self).__init__(parent)
        self.sizeCache = QSize(*size)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):

            widget = QLabel(self.parent())
            widget.resize(self.sizeCache)

            layout = QHBoxLayout()

            path = index.data()
            print(path)
            pixmap = QPixmap(path)
            lbl = QLabel(widget)
            lbl.resize(pixmap.size())
            lbl.setPixmap(pixmap)

            layout.addWidget(lbl)
            widget.setLayout(layout)
            widget.setObjectName("QTableViewDelegate")

            self.parent().setIndexWidget(
                index,
                widget
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        return self.sizeCache