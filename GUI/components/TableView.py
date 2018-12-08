from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import  QTableView, QHBoxLayout, QPushButton,\
    QFrame, QAbstractItemView, QWidget

from GUI.EventSystem import eventSystem
from GUI.components.ActionDelegate import ActionDelegate
from GUI.components.CheckBoxHeader import CheckBoxHeader
from GUI.components.FileTableModel import FileTableModel
from core.Field import Field
from functions import fileSizeConvertToFitUnit, timestampConvertToString

BUTTON_GROUP_HEIGHT = 100
class TableView(QWidget):

    def __init__(self, parent, size, specialFields=None):
        super().__init__(parent)
        self.resize(*size)
        # search Status
        self.queueFiles = []
        self.timer: QTimer = None
        self.fullResult = False

        specialFields = self.createModel(specialFields)

        tableH = size[1] - BUTTON_GROUP_HEIGHT
        self.createQTableView((size[0], tableH), specialFields)

        self._createBtnGroup((size[0], BUTTON_GROUP_HEIGHT),(0, tableH))

        self.listenEvents()
    def createModel(self,specialFields):
        if specialFields == None:
            specialFields = []
        fields = specialFields + [
                Field("fileName", "文件名", editable=True),
                Field("fileSize", "文件大小", formatMethod=fileSizeConvertToFitUnit),
                Field("createdTime", "创建时间", formatMethod=timestampConvertToString),
                Field("updatedTime", "修改时间", formatMethod=timestampConvertToString),
                Field("accessTime", "最近一次访问时间", formatMethod=timestampConvertToString),
                Field("path", "所属目录")
            ]
        specialField = self.getSpecialField(fields)
        specialFieldNames = [item.name for item in specialField]
        self.model = FileTableModel(fields, specialFieldNames)
        return specialField
    def createQTableView(self, size, specialFields):
        model = self.model
        tableView = QTableView(self)
        tableView.setFrameShape(QFrame.NoFrame)
        tableView.setMinimumSize(*size)
        for i in range(len(specialFields)):
            tableView.setItemDelegateForColumn(i + 1, specialFields[i].delegateClass(tableView))
        tableView.setModel(model)
        tableView.model = model
        tableView.setFrameShape(QFrame.NoFrame)
        tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = CheckBoxHeader()
        tableView.setHorizontalHeader(header)

        header = tableView.horizontalHeader()
        header.sectionClicked[int].connect(model.sortByField)

        model.tableView = tableView
    def listenEvents(self):
        eventSystem.listen("getPartialResult", self.getPartialResult, self)
        eventSystem.listen("finishSearch", self.finishSearch, self)
    def getSpecialField(self, fields):
        sFields = []
        for field in fields:
            if field.delegateClass is not None:
                sFields.append(field)
        return sFields

    def _createBtnGroup(self, size, movePos):
        btnWidget = QWidget(self)
        btnWidget.resize(*size)
        btnWidget.move(*movePos)

        btnLayout = QHBoxLayout()

        openChecked = QPushButton("打开选中文件", btnWidget)
        openChecked.clicked.connect(self.model.openChecked)
        btnLayout.addWidget(openChecked)

        moveChecked = QPushButton("移动选中文件", btnWidget)
        moveChecked.clicked.connect(self.model.moveChecked)
        btnLayout.addWidget(moveChecked)

        deleteButton = QPushButton("删除选中文件", btnWidget)
        deleteButton.clicked.connect(self.model.deleteChecked)
        btnLayout.addWidget(deleteButton)

        searchButton = QPushButton("开始搜索", btnWidget)
        searchButton.clicked.connect(self.clickedSearchBtn)
        self.searchButton = searchButton
        btnLayout.addWidget(searchButton)


        for btn in self.createBtnGroup():
            btnLayout.addWidget(btn)

        btnWidget.setLayout(btnLayout)
    def createBtnGroup(self):
        return []
    def getPartialResult(self, file):
        if not self.isRunInsertTimer():
            self.runInsertTimer()
        if self.fullResult:
            self.queueFiles = []
            self.model.files = []
            self.model.endResetModel()
            self.runInsertTimer()
            self.getPartialResult(file)
        else:
            self.queueFiles.append(file)
    def finishSearch(self):
        self.fullResult = True
        print("finished search")
    def clickedSearchBtn(self):
        if self.isRunInsertTimer():
            if not self.fullResult:
                eventSystem.dispatch("stopSearch")
            self.finishInsert()
        else:
            eventSystem.dispatch("triggerForm")
    def finishInsert(self):
        self.stopInsertTimer()
        self.searchButton.setText("重新搜索")
    def isRunInsertTimer(self):
        return self.timer is not None
    def runInsertTimer(self):
        timer = QTimer()
        timer.timeout.connect(self.insertItem)
        timer.start(100)
        self.searchButton.setText("停止搜索")
        self.fullResult = False
        self.timer = timer
    def insertItem(self):
        if len(self.queueFiles) > 0:
            self.model.insertRow(self.queueFiles.pop())
        else:
            if self.fullResult:
                self.finishInsert()
    def stopInsertTimer(self):
        self.timer.stop()
        self.timer = None
        self.fullResult = True
    def insert(self):
        if len(self.queueFiles) > 0:
            self.model.insertRow(self.queueFiles.pop())
    def resizeColumns(self):
        for tableView in (self.tableView,):
            for column in range(len(self.model.fields)):
                tableView.resizeColumnToContents(column)