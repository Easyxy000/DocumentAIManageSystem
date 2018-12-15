from GUI.main.EventSystem import eventSystem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from core.RepeatFileSearchThread import RepeatFileSearchThread
from GUI.public.functions import getBtn, PRIMARY

WAITING, SEARCHING = range(2)
class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.initUI("重复文件检测",topMargin=120, bottomMargin=250)
        eventSystem.listen("stopSearch", self.stopSearch, self)
        eventSystem.listen("researchRepeatDetect", self.research, self)
    def createFieldGroup(self):
        self.createGroup(self.createRootDirctoryChoose, "搜索根目录", 'root')
    def stopSearch(self):
        if self.worker is not None:
            self.worker.quit()
            self.worker.wait()
    def getBtns(self):
        submitButton = getBtn(PRIMARY, "开始搜索", self)
        submitButton.clicked.connect(self.research)
        self.submitButton = submitButton
        return [
            submitButton
        ]
    def reset(self):
        self.searching = False
        self.worker = None
        self.submitButton.setText("重新搜索")
    def research(self):
        if self.searching:
            eventSystem.dispatch("stopSearch")
            self.worker.quit()
            self.worker.wait()
            self.reset()
        else:
            self.searching = True
            self.submitButton.setText("停止搜索")
            eventSystem.dispatch("triggerResultPanel")
            self.worker = self._search(self.getForm())
            self.worker.finishedTrigger.connect(self.reset)
    def _search(self, rawData):
        worker = RepeatFileSearchThread()
        worker.initialize(rawData["root"])
        worker.start()
        worker.finishedTrigger.connect(lambda results: eventSystem.dispatch("finishRepeatSearch", results))
        self.worker = worker
        print("search!")
        return worker