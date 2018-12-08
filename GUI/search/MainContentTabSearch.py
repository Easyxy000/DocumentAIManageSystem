from GUI.EventSystem import eventSystem
from GUI.MainContentTab import MainContentTab
from PyQt5.QtWidgets import QLabel, QCheckBox, QButtonGroup, QLineEdit, QGridLayout, QHBoxLayout, \
    QComboBox, QPushButton, QFileDialog, QTableView, QVBoxLayout, QRadioButton, QWidget
from PyQt5.Qt import Qt, QTimer
from GUI.components.FileTableModel import FileTableModel
from GUI.components.FormItem import FormItem
from GUI.components.FormTable import FormTable
from GUI.components.DateLineEdit import DateLineEdit
from GUI.components.TableView import TableView
from GUI.search.SearchResult import SearchResult
from core.Field import Field
from core.SearchThread import SearchThread
from functions import config, getUserRoot, fileSizeConvertToFitUnit, timestampConvertToString
from core.FileSearch import FileSearcher

class MainContentTabSearch(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'search')
        self.createFormAndResult(Form, SearchResult)
class Form(FormTable):
    def __init__(self, p):
        super().__init__(p)
        self.form = {}
        self.checkedType = {}
        self.initUI()
        self.searcher = None
        self.searching = False
    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(20, 0, 20, 0)
        self.worker : SearchThread = None
        self.grid = grid
        self.row = 0
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'root')
        self.createGroup(self.createKeywordsGroup, "关键词", 'keywords',3)
        self.createGroup(self.createTypeGroup, "文件类型", 'fileType', 2)
        self.createGroup(self.createExtensionGroup, "文件后缀名", "fileExtension")
        self.createGroup(self.createSizeFilter, "文件大小", "fileSize", 6)
        self.createGroup(self.createTimeFilter, "创建日期", "createdDate", 6, "created")
        self.createGroup(self.createTimeFilter, "修改日期", "updatedDate", 6, "updated")
        self.createGroup(self.createTimeFilter, "访问日期", "accessDate", 6, "access")
        self.createButtonGroup()
        self.setLayout(grid)

        eventSystem.listen("stopSearch", self.stopSearch, self)
    def stopSearch(self):
        if self.worker is not None:
            self.worker.quit()
            self.worker.wait()
    def createKeywordsGroup(self):
        input = QLineEdit()

        widget = QWidget(self)
        layout = QHBoxLayout()

        containAll = QRadioButton("包含所有关键词", widget)
        containAny = QRadioButton("包含其中一个关键词", widget)

        group = QButtonGroup(self)
        containAll.setChecked(True)
        group.addButton(containAll, 1)
        group.addButton(containAny, 2)


        layout.setSpacing(0)
        layout.addWidget(containAll)
        layout.addWidget(containAny)

        widget.setLayout(layout)
        widget.setObjectName("checkedGroup")

        return (
            FormItem(input, getVal=input.text, id="keywords", col=2),
            FormItem(QLabel("(多个关键词用逗号隔开)", self), col=1),
            FormItem(widget,col=3, getVal=group.checkedId, id="method")
        )
    def createTypeGroup(self):
        types = config('search.types')
        typeExtensions = config('search.typeExtensions')
        fs = []
        for id in types:
            self.checkedType.setdefault(id, False)
            def setStated(state):
                self.checkedType[id] = state == Qt.Checked
            name = "{0}({1}{2})".format(
                types[id],
                ", ".join(["." + item for item in typeExtensions[id][:5]]),
                "..." if len(typeExtensions) > 5 else ""
            )
            cb = QCheckBox(name, self)
            cb.stateChanged.connect(setStated)
            fs.append(FormItem(cb, lambda : self.checkedType[id], id))
        return fs
    def createExtensionGroup(self):
        suffixEdit = QLineEdit(self)
        return (FormItem(suffixEdit, suffixEdit.text, col=3), FormItem(QLabel("(多个文件后缀名用逗号隔开)", self),col=1))
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
    def createTimeFilter(self, field):
        return (
            FormItem(QLabel("从", self)),
            self.getDatePickerBtns("from"),
            FormItem(QLabel("到", self)),
            self.getDatePickerBtns("to"),
        )
    def getDatePickerBtns(self, valueKey):
        textLine = DateLineEdit()
        return FormItem(textLine, textLine.getDate, valueKey)
    def createCreatedTimeGroup(self):
        pass
    def createButtonGroup(self):
        submitButton = QPushButton("开始搜索", self)

        submitButton.clicked.connect(self.research)

        similarSearchBtn = QPushButton("相似图片搜索", self)
        similarSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "similarImageSearch"))

        resetButton = QPushButton("重置", self)
        grid = QHBoxLayout()
        for widget in (submitButton,  resetButton, similarSearchBtn):
            grid.addWidget(widget)
        self._createButtonGroup(grid)
        self.submitButton = submitButton
    def research(self):
        def reset():
            self.searching = False
            self.worker = None
            # self.filterButton.setDisabled(True)
            self.submitButton.setText("重新搜索")
        if self.searching:
            eventSystem.dispatch("stopSearch")
            self.worker.quit()
            self.worker.wait()
            reset()
        else:
            self.searching = True
            self.submitButton.setText("停止搜索")
            eventSystem.dispatch("triggerResult")
            self.worker = self._search(self.getForm())
            self.worker.finishedTrigger.connect(reset)
    def _search(self, rawData, filterInResult=False):
        searcher = FileSearcher() if self.searcher is None else self.searcher

        keywords = rawData["keywords"]
        if keywords["keywords"] != "" :
            formatKeywords = []
            for item in keywords["keywords"].split(","):
                if item == "" : continue
                formatKeywords.append(item)
            searcher.setKeywordFilter(formatKeywords, containAll=keywords["method"] == 1)
        fileSize = rawData["fileSize"]
        min, max = self.unitFormat(fileSize["minVal"], fileSize["minUnit"]), self.unitFormat(fileSize["maxVal"], fileSize["maxUnit"])
        if min is not None or max is not None:
            searcher.setFileSizeFilter(
                min=min,
                max=max
            )
        for fun, field in zip((searcher.setCreatedTimeFilter, searcher.setUpdatedTimeFilter, searcher.setAccessTimeFilter), ("created", "updated", "access")):
            data = rawData[field + "Date"]
            fromTime, toTime = self.QdateConvertoTime(data["from"]), self.QdateConvertoTime(data["to"])
            if fromTime is not None or toTime is not None:
                fun(start=fromTime, end=toTime)

        typeExtensions = config("search.typeExtensions")
        extensions = set()
        fileType = rawData["fileType"]
        for type in fileType:
            if fileType[type] == True:
                for item in typeExtensions[type]:
                    extensions.add(item)

        if rawData["fileExtension"] != "":
            for item in rawData["fileExtension"].split(","):
                if item == "" : continue
                if item[0] == "." : item = item[1:]
                extensions.add(item.lower())

        if len(extensions) > 0: searcher.setExtensionFilter(extensions)

        worker = SearchThread()
        worker.initialize(searcher, rawData["root"])
        worker.start()
        worker.putResultTrigger.connect(lambda item: eventSystem.dispatch("getPartialResult", item))
        worker.finishedTrigger.connect(lambda : eventSystem.dispatch("finishSearch"))

        self.worker = worker
        self.searcher = searcher

        print("search!")
        return worker
