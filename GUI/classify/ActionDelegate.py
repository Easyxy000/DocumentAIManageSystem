from PyQt5.Qt import QSize
from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout


class ActionDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ActionDelegate, self).__init__(parent)
        self.sizeCache = QSize(200, 40)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            widget = QWidget()

            layout = QHBoxLayout()

            openBtn = QPushButton("打开",widget)
            openBtn.clicked.connect(lambda : self.parent().model.open(index.row()))
            openBtn.setObjectName("tableViewPrimaryBtn")

            editBtn = QPushButton("修改分类",widget)
            editBtn.clicked.connect(lambda : self.parent().model.open(index.row()))
            editBtn.setObjectName("tableViewWarningBtn")

            layout.addWidget(openBtn)
            layout.addWidget(editBtn)
            widget.setLayout(layout)

            widget.setObjectName("QTableViewDelegate")
            self.parent().setIndexWidget(
                index,
                widget
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        return self.sizeCache