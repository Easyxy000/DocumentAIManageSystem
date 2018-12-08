from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QPushButton

from GUI.EventSystem import eventSystem
from GUI.MainContentTab import MainContentTab
from GUI.components.FormTable import FormTable
from GUI.search.SimilarSearchResult import SimilarSearchResult
from core.SearchThread import SearchThread
from core.SimilarImageSearchThread import SimilarImageSearchThread

class SimilarImageSearch(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'similarImageSearch')
        self.createFormAndResult(Form, SimilarSearchResult)

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
        self.createGroup(self.createRootDirctoryChoose, "搜索文件", 'compareObj',None, "file")
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'searchRoot')
        self.setLayout(grid)

        Hbox = QHBoxLayout()
        searchBtn = QPushButton("开始搜索", self)
        normalFileSearchBtn = QPushButton("一般文件搜索", self)


        searchBtn.clicked.connect(self.search)
        normalFileSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "search"))
        Hbox.addWidget(searchBtn)
        Hbox.addWidget(normalFileSearchBtn)

        self._createButtonGroup(Hbox)
    def search(self):
        eventSystem.dispatch("triggerResult")
        workThread = SimilarImageSearchThread()
        data = self.getForm()
        workThread.initialize(data["compareObj"], data["searchRoot"])
        workThread.start()
        workThread.finishedTrigger.connect(lambda results: eventSystem.dispatch("finishedSimilarImageSearch", results))
        self.workThread = workThread

