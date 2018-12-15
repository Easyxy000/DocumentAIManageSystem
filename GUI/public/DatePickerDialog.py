from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QCalendarWidget, QLabel, QDialog, \
    QPushButton, QDesktopWidget
from PyQt5.QtCore import QDate
from PyQt5.Qt import Qt
class DatePickerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.clear = False
    # self.exec()
    def initUI(self):
        VBox = QVBoxLayout()
        calendar = QCalendarWidget(self)
        calendar.setGridVisible(True)
        # calendar.move(20, 20)
        calendar.clicked[QDate].connect(self.showDate)

        label = QLabel(self)
        date = calendar.selectedDate()
        label.setText(self.getDate(date))
        # label.move(130, 260)
        label.setAlignment(Qt.AlignCenter)
        self.label = label

        self.calendar = calendar


        VBox.addWidget(calendar, 5)
        VBox.addWidget(label, 1)

        self.setLayout(VBox)

        clearButton = QPushButton("不限", self)
        confirmButton = QPushButton("选择", self)
        cancelButton = QPushButton("取消", self)
        clearButton.clicked.connect(self.clearCallback)
        confirmButton.clicked.connect(self.acceptCallback)
        cancelButton.clicked.connect(self.reject)
        Hbox = QHBoxLayout()
        Hbox.addWidget(clearButton)
        Hbox.addWidget(confirmButton)
        Hbox.addWidget(cancelButton)

        VBox.addLayout(Hbox)


        self.resize(350, 300)
        self.center()
        self.setWindowTitle('日历控件')
        self.show()
    def acceptCallback(self):
        self.clear = False
        self.accept()
    def clearCallback(self):
        self.clear = True
        self.accept()
    def showDate(self, date : QDate):
        self.label.setText(self.getDate(date))
    def getDate(self, date : QDate):
        weekdata = ["一", "二", "三", "四", "五", "六", "日"]
        return "{0}年{1}月{2}日 周{3}".format(date.year(), date.month(), date.day(), weekdata[date.dayOfWeek() - 1])
    def get_data(self):  # 定义获取用户输入数据的方法
        if self.clear == True: return None
        return self.calendar.selectedDate()
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())