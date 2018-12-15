from PyQt5.Qt import QSize, QPixmap
from PyQt5.QtWidgets import QItemDelegate, QLabel, QHBoxLayout
class ThumbDelegate(QItemDelegate):
    def __init__(self, parent, size):
        super(ThumbDelegate, self).__init__(parent)
        # 初始化尺寸
        self.sizeCache = QSize(*size)
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            # 创建控件
            widget = QLabel(self.parent())
            widget.resize(self.sizeCache)
            layout = QHBoxLayout()
            widget.setLayout(layout)
            widget.setObjectName("QTableViewDelegate")

            # 创建缩略图
            path = index.data()
            pixmap = QPixmap(path)
            lbl = QLabel(widget)
            lbl.resize(pixmap.size())
            lbl.setPixmap(pixmap)

            # 将缩略图标签加入到控件中（为了居中...使用了两层控件）
            layout.addWidget(lbl)

            # 设置控件
            self.parent().setIndexWidget(
                index,
                widget
            )
    def sizeHint(self, option: 'QStyleOptionViewItem', index):
        return self.sizeCache