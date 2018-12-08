from PyQt5.Qt import Qt, QSize, QPixmap

from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QLabel

size = (100, 40)
class ThumbDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ThumbDelegate, self).__init__(parent)
        self.sizeCache = None
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            pixmap = QPixmap("cache/{0}.jpg".format(index.row()))
            lbl = QLabel(self.parent())
            lbl.resize(*size)
            lbl.setPixmap(pixmap)
            lbl.setObjectName("ThumbDelegate")
            self.parent().setIndexWidget(
                index,
                lbl
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        if self.sizeCache is None:
            size: QSize = QSize(100, 40)
        return self.sizeCache