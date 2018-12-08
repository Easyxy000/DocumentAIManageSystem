from GUI.MainContentTab import MainContentTab
from PyQt5.QtWidgets import QLabel, QFileSystemModel, QTreeView, QLineEdit, QGridLayout, QTextEdit, QHBoxLayout,QComboBox,QPushButton,QFileDialog
from PyQt5.Qt import Qt
from GUI.components.ImageButton import ImageButton
from GUI.components.FormItem import FormItem
from GUI.components.FormTable import FormTable
from functions import config, getUserRoot

class MainContentTabCheck(MainContentTab):
    def __init__(self, parent):
        super().__init__(parent, 'check')
        self.createFormAndResult(Main, Side)
class Main(QLabel):
    def __init__(self, p, size):
        super().__init__(p)
        self.initUI(size)
    def initUI(self, size):
        margin = 10
        model = QFileSystemModel()
        # model.setRootPath(config('config.defaultRoot'))
        tree = QTreeView(self)
        tree.setModel(model)
        tree.setAnimated(False)
        tree.setIndentation(20)
        tree.setSortingEnabled(True)
        tree.setWindowTitle("Dir View")
        tree.resize(size[0] - 2 * margin, size[1] - 2 * margin)
        tree.move(margin, margin)
class Side(FormTable):
    def __init__(self, p, size):
        super().__init__(p)
        self.form = {}
        self.initUI()
        self.partSize = size
        self.dateData = {}
        self.rootEdit = None
    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(20, 0, 20, 400)
        self.grid = grid
        self.row = 0
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录",None, 'root')
        self.createButtonGroup()
        self.setLayout(grid)
    def createRootDirctoryChoose(self):
        btn = QPushButton("选择", self)
        btn.clicked.connect(self.chooseRootDirctory)

        textEdit = QLineEdit(self)
        return (FormItem(btn, lambda : self.rootDirctory, None, 1), FormItem(textEdit, textEdit.text, None, 2))
    def chooseRootDirctory(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        print(fname)
        self.rootDirctory = fname
    def createButtonGroup(self):
        submitButton = QPushButton("搜索", self)
        submitButton.clicked.connect(self.getForm)
        grid = QHBoxLayout()
        for widget in (submitButton, ):
            grid.addWidget(widget)
        self.grid.addLayout(grid, self.row, 1)