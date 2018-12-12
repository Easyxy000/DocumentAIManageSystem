from PyQt5.Qt import QSize
from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout


class ActionDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ActionDelegate, self).__init__(parent)
        self.sizeCache = QSize(100, 40)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            widget = QWidget()
            widget.resize(self.sizeCache)
            layout = QHBoxLayout()

            btn = QPushButton("打开",widget)
            btn.clicked.connect(lambda : self.parent().model.open(index.row()))
            btn.setObjectName("tableViewPrimaryBtn")

            layout.addWidget(btn)
            widget.setLayout(layout)

            widget.setObjectName("QTableViewDelegate")
            self.parent().setIndexWidget(
                index,
                widget
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        return self.sizeCache