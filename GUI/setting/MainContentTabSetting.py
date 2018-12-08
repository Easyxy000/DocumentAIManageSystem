from GUI.MainContentTab import MainContentTab
from PyQt5.QtWidgets import QLabel, QFileSystemModel, QTreeView, QLineEdit, QGridLayout, QTextEdit, QHBoxLayout,QComboBox,QPushButton,QFileDialog
from PyQt5.Qt import Qt
from GUI.components.ImageButton import ImageButton
from GUI.components.FormItem import FormItem

from functions import config
from GUI.components.FormTable import FormTable
class MainContentTabSetting(MainContentTab):
    def __init__(self, parent):
        super().__init__(parent, 'setting')
        size = config('gui.windowSize')
        main = Main(self, size)
        main.resize(*size)
class Main(FormTable):
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
        grid.setContentsMargins(20, 0, 20, 200)
        self.grid = grid
        self.row = 0
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'root')
        self.createGroup(self.createKeywordsGroup, "关键词", 'keywords')
        self.createGroup(self.createTypeGroup, "文件类型", 'fileType')
        self.createGroup(self.createSuffixGroup, "文件后缀名", "fileSuffix")
        self.createGroup(self.createSizeFilter, "文件大小", "fileSize")
        self.createGroup(self.createCreatedTimeFilter, "创建日期", "createdDate")
        self.createGroup(self.createCreatedTimeFilter, "修改日期", "updatedDate")
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
    def createKeywordsGroup(self):
        input = QLineEdit()
        return FormItem(input, input.text)
    def createTypeGroup(self):
        combo = QComboBox(self)
        self.addItemsFromData(combo, config('search.types'))
        return FormItem(combo, combo.currentData)
    def createSuffixGroup(self):
        combo = QComboBox(self)
        self.addItemsFromData(combo, dict([(suffix, suffix) for suffix in config('search.suffixes')]))
        suffixEdit = QLineEdit(self)
        return (FormItem(combo, combo.currentData,"selected", 1), FormItem(suffixEdit, suffixEdit.text, "text", 2))
    def addItemsFromData(self, combo, items):
        for key in items:
            combo.addItem(items[key], key)
    def createSizeFilter(self):
        units = dict([(item, item) for item in config("search.units")])
        minSizeVal = QLineEdit(self)
        minSizeUnit = QComboBox(self)
        self.addItemsFromData(minSizeUnit, units)

        maxSizeVal = QLineEdit(self)
        maxSizeUnit = QComboBox(self)
        self.addItemsFromData(maxSizeUnit, units)

        return (
            FormItem(QLabel("从", self)),
            FormItem(minSizeVal, minSizeVal.text, "minVal"),
            FormItem(minSizeUnit, minSizeUnit.currentData, "minUnit"),
            FormItem(QLabel("到", self)),
            FormItem(maxSizeVal, maxSizeVal.text, "maxVal"),
            FormItem(maxSizeUnit, maxSizeUnit.currentData, "maxUnit")
        )
    def createCreatedTimeFilter(self):
        fromBtn = QPushButton("选择", self)
        formCancelBtn = QPushButton("不限", self)
        formCancelBtn.setDisabled(True)

        toBtn = QPushButton("选择", self)
        toCancelBtn = QPushButton("不限", self)
        toCancelBtn.setDisabled(True)

        return (FormItem(fromBtn), FormItem(formCancelBtn), FormItem(toBtn), FormItem(toCancelBtn))
    def getDatePickerBtnCallBack(self, chooseBtn, cancelBtn, valueKey):
        def chooseClick():
            pass
        def cancelClick():
            pass
        return chooseClick, cancelClick

    def createCreatedTimeGroup(self):
        pass
    def createButtonGroup(self):
        submitButton = ImageButton("提交", config('UIElements.buttonNormal'), self)
        submitButton.clicked.connect(self.getForm)
        resetButton = ImageButton("重置", config('UIElements.buttonNormal'), self)
        grid = QHBoxLayout()
        for widget in (submitButton, resetButton):
            grid.addWidget(widget)
        self.grid.addLayout(grid, self.row, 1)