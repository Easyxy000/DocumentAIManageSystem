import random

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFrame

from GUI.main.EventSystem import eventSystem
from core.FileSearch import FileSearcher
from core.Field import Field
from demo.myView.FileTableModel import FileTableModel
from demo.myView.ActionDelegate import ActionDelegate
from demo.myView.MyTreeView import MyTreeView
from GUI.public.functions import fileSizeConvertToFitUnit, timestampConvertToString


class MainForm(QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.id = 0
        self.clearResult = True
        self.queueFiles = []
        self.timer : QTimer = None
        self.setObjectName("mainWindow")
        self.setStyleSheet("""
#mainWindow{
    background-color:#f7f9fc;
}
QHeaderView{
    padding:0;
    margin:0;
    
}
QHeaderView::section { 
    background-color:#f7f9fc;
    border: 0; 
    color: #6d6f72; 
}
QTableView::item,#QTableViewDelegate{ 
    background-color:#f7f9fc;
    border:0;
    min-height: 200px;
}

QTableView::item:hover { 
    background-color: #dae2f0;
}
#tableViewOpenBtn{
    margin: 0 auto;
}
        
        """)
        layout = QVBoxLayout()
        fields = [
            Field("action", "操作", editable=True, delegateClass=ActionDelegate),
            Field("fileName", "文件名", editable=True),
            Field("fileSize", "文件大小", formatMethod=fileSizeConvertToFitUnit),
            Field("createdTime", "创建时间",  formatMethod=timestampConvertToString),
            Field("updatedTime", "修改时间", formatMethod=timestampConvertToString),
            Field("accessTime", "最近一次访问时间", formatMethod=timestampConvertToString),
            Field("path", "所属目录")
        ]
        model = FileTableModel(fields, ["操作"])
        tableView = MyTreeView(model, fields)
        tableView.setFrameShape(QFrame.NoFrame)
        tableView.setMaximumSize(800, 400)
        tableView.setItemDelegateForColumn(1, ActionDelegate(tableView))

        header = tableView.horizontalHeader()
        header.sectionClicked[int].connect(self.sortTable)




        layout.addWidget(tableView)
        self.setLayout(layout)

        Hbox = QHBoxLayout()

        openChecked = QPushButton("打开选中文件", self)
        openChecked.clicked.connect(model.openChecked)
        Hbox.addWidget(openChecked)

        moveChecked = QPushButton("移动选中文件", self)
        moveChecked.clicked.connect(model.moveChecked)
        Hbox.addWidget(moveChecked)

        deleteButton = QPushButton("删除选中文件", self)
        deleteButton.clicked.connect(model.deleteChecked)
        Hbox.addWidget(deleteButton)

        searchButton = QPushButton("停止搜索", self)
        searchButton.clicked.connect(self.clickedSearchBtn)



        layout.addLayout(Hbox)

        self.tableView = tableView
        self.model = model
        self.setMinimumSize(800, 600)
        self.initialLoad()

        # timer = QTimer()
        # timer.timeout.connect(self.generate)
        # timer.start(1000)
        # self.timer = timer
        eventSystem.listen("getPartialResult", self.getPartialResult, self)
        eventSystem.listen("finishClassify", self.finishSearch, self)
        eventSystem.listen("stopSearch", self.stopSearch, self)
        self.tableView = tableView
        self.model = model
    def stopSearch(self):
        if self.timer is None: return
        self.timer.stop()
        self.timer = None
    def getPartialResult(self, file):
        if self.clearResult:
            self.queueFiles = []
            self.model.files = []
            self.model.endResetModel()
            self.model.dirty = False
            self.clearResult = False
            self.runInsertTimer()
            self.getPartialResult(file)
        else:
            self.queueFiles.append(file)
        #     return
        # if self.model.rowCount() > 200:
        #     return
        # self.model.insertRow(file)
        # self.resizeColumns()
    def runInsertTimer(self):
        timer = QTimer()
        timer.timeout.connect(self.insert)
        timer.start(50)
        self.timer = timer
    def insert(self):
        if len(self.queueFiles) > 0:
            self.model.insertRow(self.queueFiles.pop())
    def finishSearch(self):
        self.clearResult = True
        # self.timer.stop()
        # self.timer = None
        print("finished")
    def clickedSearchBtn(self):
        pass
    def generate(self):
        print("generate")
        self.model.insertRow(self.generateItem())
    def initialLoad(self):
        files = []
        searcher = FileSearcher()
        searcher.setPath("/users/xushaojun/Documents/吉他谱")
        for item in searcher.search():
            files.append(item)
        self.model.load(files)
        self.resizeColumns()

    def resizeColumns(self):
        for tableView in (self.tableView, ):
            for column in range(6):
                tableView.resizeColumnToContents(column)
    def sortTable(self, section):
        if section == 0:
            return
        print("sorted")
        self.model.sortByField(section - 1)
    def generateItem(self):
        exts = ["jpg", "png","bmp","psd","gif"]
        dirs = ["薛之谦","徐秉龙", "余佳运"]
        name = "吉他谱{0}.{1}".format(self.id,exts[random.randint(0,4)] )
        self.id += 1
        return {
             "fileSize": 386958,
            "createdTime": 1543762154.0 - random.randint(50000,100000),
            "updatedTime": 1543762149.0 - random.randint(0,50000),
            "accessTime": 1543762149.0 - random.randint(25000,50000),
            "fileName": name,
             "path" : "﻿/Users/xushaojun/Documents/吉他谱/{0}".format(dirs[random.randint(0,2)])}
    def generateItems(self, count):
        files = []
        for i in range(count):
            file = self.generateItem()
            childCount = random.randint(1,5)
            # file["children"] = [ self.generateItem() for j in range(childCount)]
            files.append(file)
        return files
