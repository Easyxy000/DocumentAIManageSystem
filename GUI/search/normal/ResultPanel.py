from PyQt5.QtCore import QTimer

from GUI.main.EventSystem import eventSystem
from GUI.public.ActionDelegate import ActionDelegate
from GUI.public.AbstractResultPanel import AbstractResultPanel
from core.Field import Field
from GUI.public.functions import getBtn, INFO, DEFAULT, PRIMARY

WAITING, SEARCHING = range(2)
class ResultPanel(AbstractResultPanel):
    def __init__(self, p, size):
        super().__init__(p, size,[
            Field("action", "操作", editable=True, hasValue=False, delegateClass=ActionDelegate),
        ])
        self.queueFiles = []
        self.timer: QTimer = None
        self.fullResult = False
        self.firstInsert = True
        self.setObjectName("normalSearchResult")
        self.submitState = None
    def listenEvents(self):
        eventSystem.listen("startInsert", self.runInsertTimer, self)
        eventSystem.listen("getPartialResult", self.getPartialResult, self)
        eventSystem.listen("finishNormalSearch", self.finishNormalSearch, self)
        eventSystem.listen("notifyStop", lambda : self.submitBtn.setText("重新搜索"), self)
        eventSystem.listen("notifyFilterResult", self.notifyFilterResult, self)
    def getBtns(self):
        similarSearchBtn = getBtn(INFO,"相似图片搜索")
        similarSearchBtn.clicked.connect(lambda : eventSystem.dispatch("changeTab", "similarImageSearch"))

        submitBtn = getBtn(PRIMARY, "开始搜索")
        submitBtn.clicked.connect(self.clickedSubmit)

        self.submitBtn = submitBtn
        filterBtn = getBtn(DEFAULT,"在结果中筛选")
        filterBtn.clicked.connect(self.clickedFilter)
        return [
            submitBtn,
            filterBtn,
            similarSearchBtn
        ]
    def clickedFilter(self):
        eventSystem.dispatch("triggerFormPanel")
        eventSystem.dispatch("notifyFilter", self.model.files)
    def runInsertTimer(self):
        self.model.beginResetModel()
        self.model.files = []
        self.model.endResetModel()

        timer = QTimer()
        timer.timeout.connect(self.insert)
        timer.start(100)
        self.setSubmitState(SEARCHING)
        self.fullResult = False
        self.timer = timer
    def insert(self):
        if len(self.queueFiles) > 0:
            self.model.insertRow(self.queueFiles.pop())
        elif self.fullResult:
            self.stopInsertTimer()
    def stopInsertTimer(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
            self.fullResult = False
    def getPartialResult(self, file):
        self.queueFiles.append(file)
    def finishNormalSearch(self):
        self.fullResult = True
        print("finished search")
    def clickedSubmit(self):
        state = self.submitState
        if state == WAITING:
            eventSystem.dispatch("triggerFormPanel")
        elif state == SEARCHING:
            self.setSubmitState(WAITING)
            eventSystem.dispatch("stopSearch")
            self.stopInsertTimer()
    def setSubmitState(self, state):
        if state == WAITING:
            self.submitBtn.setText("开始搜索")
        elif state == SEARCHING:
            self.submitBtn.setText("停止搜索")
        self.submitState = state
    def notifyFilterResult(self, results):
        print(results)
        self.model.beginResetModel()
        self.model.files = results
        self.model.endResetModel()

