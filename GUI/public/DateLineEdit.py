from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLineEdit
from GUI.public.DatePickerDialog import DatePickerDialog
class DateLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def __init__(self, clickEvents):
        super().__init__()
        self.datePickerDialog = None
        self.date = None
        self.clickEvents = clickEvents
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            v = self.datePickerDialog if self.datePickerDialog is not None else DatePickerDialog()
            if v.exec_():  # 执行方法，成为模态对话框，用户点击OK后，返回1
                date = v.get_data()
                if date == None:
                    self.setText("")
                else:
                    self.setText("{0}-{1}-{2}".format(date.year(), date.month(), date.day()))
                self.date = date
                for event in self.clickEvents:
                    print("call event")
                    event()
    def getDate(self):
        return self.date