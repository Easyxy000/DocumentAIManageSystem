from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    # self.exec()
    def initUI(self):
        self.setWindowTitle("新建小组")  # 窗口标题
        self.setGeometry(400, 400, 200, 200)  # 窗口位置与大小

        self.lab_a = QLabel('小组名称:')
        self.lab_b = QLabel('竞赛项目:')

        self.name_edit = QLineEdit()  # 用于接收用户输入的单行文本输入框
        self.game_item = QComboBox()  # 建立一个下拉列表框

        for name, id in zip(["a", "b", "c"], [1, 2, 3]):  # 为下拉列表框添加选择项（从数据库中查询取得）
            self.game_item.addItem(name, id)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)  # 窗口中建立确认和取消按钮

        self.glayout = QGridLayout()

        self.glayout.addWidget(self.lab_a, 0, 0)
        self.glayout.addWidget(self.lab_b, 1, 0)
        self.glayout.addWidget(self.name_edit, 0, 1)
        self.glayout.addWidget(self.game_item, 1, 1)

        self.glayout.addWidget(self.buttons, 2, 1)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setLayout(self.glayout)
    def get_data(self):  # 定义获取用户输入数据的方法
        return self.name_edit.text(), self.game_item.itemData(self.game_item.currentIndex())

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
        v = MyDialog()  # 建立对话框实例
        if v.exec_():  # 执行方法，成为模态对话框，用户点击OK后，返回1
            name, game = v.get_data()
            print(name)
            print(game)
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())