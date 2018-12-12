import sys
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QWidget, QCalendarWidget, QLabel, QDialog, \
    QPushButton, QDesktopWidget, QGridLayout, QDialogButtonBox
from PyQt5.QtCore import QDate
from PyQt5.Qt import Qt


class DatePickerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
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

        Hbox = QHBoxLayout()


        VBox.addWidget(calendar, 5)
        VBox.addWidget(label, 1)

        self.setLayout(VBox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)  # 窗口中建立确认和取消按钮

        VBox.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.resize(350, 300)
        self.center()
        self.setWindowTitle('日历控件')
        self.show()
    def showDate(self, date : QDate):
        self.label.setText(self.getDate(date))
    def getDate(self, date : QDate):
        weekdata = ["一", "二", "三", "四", "五", "六", "日"]
        return "{0}年{1}月{2}日 周{3}".format(date.year(), date.month(), date.day(), weekdata[date.dayOfWeek() - 1])
    def get_data(self):  # 定义获取用户输入数据的方法
        return self.calendar.selectedDate()
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.resize(250, 150)
        self.center()

        self.setWindowTitle('Center')
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        button = QPushButton("弹出", self)
        button.clicked.connect(self.tirrger)
        self.show()

    def tirrger(self):
        v = DatePickerDialog()  # 建立对话框实例
        if v.exec_():  # 执行方法，成为模态对话框，用户点击OK后，返回1
            print(v.get_data())
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())