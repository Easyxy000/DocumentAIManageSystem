from PyQt5.Qt import QSize, QLabel, QDesktopWidget, Qt

from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout, QDialog

from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractResultPanel import AbstractResultPanel, config
from GUI.public.ActionDelegate import ActionDelegate
from core.Field import Field


class RepeatChildrenDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(RepeatChildrenDelegate, self).__init__(parent)
        self.sizeCache = QSize(100, 40)
        self.w = int(self.parent().size().width() * 0.95)
        self.dialog = MyDialog(self.w)
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
        dialog = self.dialog
        h = 50 * len(data["children"]) + 130 + config('gui.topBorderHeight')

        dialog.load(data["children"], self.w, h)
        if dialog.exec_():  # 执行方法，成为模态对话框，用户点击OK后，返回1
            eventSystem.dispatch("addChildrenCheckList", row, dialog.getCheckedList())
class MyDialog(QDialog):
    def __init__(self, w):
        super().__init__()
        self.initUI(w)
    # self.exec()
    def initUI(self, w):
        h = 100
        self.resize(w, h)
        self.center()
        self.setWindowTitle("查看重复项")  # 窗口标题
        self.setWindowFlags(Qt.FramelessWindowHint)

        topBorderH = config('gui.topBorderHeight')
        topBorder = self.createTopBorder(w, topBorderH)


        panel = ResultPanel(self, (w, h - 20))
        panel.move(0, topBorderH)

        self.panel = panel
        self.setObjectName("repeatWindow")
        self.setStyleSheet(config("globalStyleSheet"))
    def load(self, items, w, h):
        panel = self.panel
        panel.model.load(items)
        self.resize(w, h)
        panel.resize(w, h)

        tableH = 50 * len(items) + 30
        panel.tableView.resize(w, tableH)

        btnGroupWidget = self.panel.btnGroupWidget
        btnGroupWidget.move(0, tableH + config('gui.topBorderHeight'))

        self.center()
    def getCheckedList(self):
        return self.panel.model.checkList
    def createTopBorder(self, w, h):

        topBorder = QLabel(self)
        topBorder.resize(w, h)

        btnSize = config("gui.topBorderBtnSize")

        closeBtn = QPushButton(topBorder)
        closeBtn.setObjectName("topBorderCloseBtn")
        closeBtn.clicked.connect(self.close)

        btns = (closeBtn,)

        margin = config("gui.topBorderBtnMargin")
        marginRight = config("gui.topBorderBtnMarginRight")
        x = w - len(btns) * (btnSize[0] + margin) + margin - marginRight
        y = config("gui.topBorderBtnMarginTop")
        for btn in btns:
            btn.move(x, y)
            x += margin + btnSize[0]
        return topBorder
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", hasValue=False, delegateClass=ActionDelegate),
        ],closeFields=["accessTime","updatedTime"])
    def getBtns(self):
        return []