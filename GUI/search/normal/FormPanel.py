from GUI.main.EventSystem import eventSystem
from PyQt5.QtWidgets import QLabel, QCheckBox, QButtonGroup, QLineEdit, \
    QHBoxLayout, QComboBox, QRadioButton
from PyQt5.Qt import Qt
from GUI.public.FormItem import FormItem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from GUI.public.DateLineEdit import DateLineEdit
from core.SearchThread import SearchThread
from GUI.public.functions import config, PRIMARY, INFO, DEFAULT
from core.FileSearch import FileSearcher
from GUI.public.functions import getBtn
WAITING, SEARCHING, FILTER = range(3)
class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.checkedType = {}
        self.submitState = WAITING
        self.worker : SearchThread = None
        self.initUI("文件高级搜索")
        eventSystem.listen("stopSearch", self.stopSearch, self)
        eventSystem.listen("setSubmitState", self.setSubmitState,self)
        eventSystem.listen("notifyFilter", self.notifyFilter, self)
    def createFieldGroup(self):
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'root')
        self.createGroup(self.createKeywordsGroup, "关键词", 'keywords',3)
        self.createGroup(self.createTypeGroup, "文件类型", 'fileType', 2)
        self.createGroup(self.createExtensionGroup, "文件后缀名", "fileExtension")
        self.createGroup(self.createSizeFilter, "文件大小", "fileSize", 6)
        self.createGroup(self.createTimeFilter, "创建日期", "createdDate", 6, "created")
        self.createGroup(self.createTimeFilter, "修改日期", "updatedDate", 6, "updated")
        self.createGroup(self.createTimeFilter, "访问日期", "accessDate", 6, "access")
    def createKeywordsGroup(self):
        input = QLineEdit()

        label = QLabel(self)
        layout = QHBoxLayout()

        containAll = QRadioButton("包含所有关键词", label)
        containAny = QRadioButton("包含其中一个关键词", label)

        group = QButtonGroup(self)
        containAll.setChecked(True)
        group.addButton(containAll, 1)
        group.addButton(containAny, 2)


        layout.setSpacing(0)
        layout.addWidget(containAll)
        layout.addWidget(containAny)

        label.setLayout(layout)
        label.setObjectName("checkedGroup")

        return (
            FormItem(input, getVal=input.text, id="keywords", col=2),
            FormItem(QLabel("(多个关键词用逗号隔开)", self), col=1),
            FormItem(label,col=3, getVal=group.checkedId, id="method")
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
                ", ".join(["." + item for item in typeExtensions[id][:3]]),
                "..." if len(typeExtensions) > 3 else ""
            )
            cb = QCheckBox(name, self)
            cb.stateChanged.connect(setStated)
            fs.append(FormItem(cb, lambda : self.checkedType[id], id))
        return fs
    def createExtensionGroup(self):
        suffixEdit = QLineEdit(self)
        return (FormItem(suffixEdit, suffixEdit.text, col=3), FormItem(QLabel("(多个文件后缀名用逗号隔开)", self),col=1))
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
        label = QLabel(self)
        group = QButtonGroup(self)
        layout = QHBoxLayout()
        layout.setSpacing(0)

        for i, text in enumerate(("7天内","30天内", "不限")):
            radio = QRadioButton(text, label)
            group.addButton(radio, i)
            layout.addWidget(radio)
            if text == "不限":
                radio.setChecked(True)

        label.setLayout(layout)
        label.setObjectName("checkedTimeGroup")
        return (
            FormItem(label),
            FormItem(QLabel("从", self)),
            self.getDatePickerBtns("from", group),
            FormItem(QLabel("到", self)),
            self.getDatePickerBtns("to", group),
        )
    def getDatePickerBtns(self, valueKey, checkedGroup : QButtonGroup):
        textLine = DateLineEdit([self.getDateLineChange(checkedGroup)])
        return FormItem(textLine, textLine.getDate, valueKey)
    def getDateLineChange(self, group: QButtonGroup):
        def change():
            print(group)
            print(group.checkedId())
            for item in group.children():
                print(item.text())
            group.checkedButton().setChecked(False)
        return change
    def createCreatedTimeGroup(self):
        pass
    def getBtns(self):
        submitButton = getBtn(PRIMARY, "开始搜索", self)
        submitButton.clicked.connect(self.clickedSubmit)

        similarSearchBtn = getBtn(INFO, "相似图片搜索", self)
        similarSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "similarImageSearch"))

        resetButton = getBtn(DEFAULT, "重置", self)

        self.submitButton = submitButton
        return (submitButton,  resetButton, similarSearchBtn)
    def notifyFilter(self, items):
        print(items)
        self.lastItems = items
        self.setSubmitState(FILTER)
    def stopSearch(self):
        if self.worker is not None:
            self.worker.quit()
            self.worker.wait()
            self.worker = None
            self.setSubmitState(WAITING)
            eventSystem.dispatch("notifyStop")
    def setSubmitState(self, state):
        if state == WAITING:
            self.submitButton.setText("开始搜索")
        elif state == SEARCHING:
            self.submitButton.setText("停止搜索")
        elif state == FILTER:
            self.submitButton.setText("开始筛选")
        self.submitState = state
    def getSearcher(self):
        searcher = FileSearcher()
        rawData = self.getForm()
        keywords = rawData["keywords"]
        if keywords["keywords"] != "":
            formatKeywords = []
            for item in keywords["keywords"].split(","):
                if item == "": continue
                formatKeywords.append(item)
            searcher.setKeywordFilter(formatKeywords, containAll=keywords["method"] == 1)
        fileSize = rawData["fileSize"]
        min, max = self.unitFormat(fileSize["minVal"], fileSize["minUnit"]), self.unitFormat(fileSize["maxVal"],
                                                                                             fileSize["maxUnit"])
        if min is not None or max is not None:
            searcher.setFileSizeFilter(
                min=min,
                max=max
            )
        for fun, field in zip(
                (searcher.setCreatedTimeFilter, searcher.setUpdatedTimeFilter, searcher.setAccessTimeFilter),
                ("created", "updated", "access")):
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
                if item == "": continue
                if item[0] == ".": item = item[1:]
                extensions.add(item.lower())

        if len(extensions) > 0: searcher.setExtensionFilter(extensions)
        searcher.setPath(rawData["root"])
        return searcher
    def clickedSubmit(self):
        state = self.submitState
        if state == WAITING:
            self.search()
        elif state == SEARCHING:
            self.stopSearch()
        elif state == FILTER:
            self.filter()
        eventSystem.dispatch("triggerResultPanel")
    def filter(self):
        search = self.getSearcher()
        print("lastItem len {0}".format(len(self.lastItems)))
        eventSystem.dispatch("notifyFilterResult", search.filterItems(self.lastItems))
    def search(self):
        searcher = self.getSearcher()
        worker = SearchThread()
        worker.initialize(searcher)
        worker.start()
        eventSystem.dispatch("startInsert")
        worker.putResultTrigger.connect(lambda item: eventSystem.dispatch("getPartialResult", item))
        worker.finishedTrigger.connect(lambda : eventSystem.dispatch("finishNormalSearch"))
        self.worker = worker