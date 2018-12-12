from GUI.main.MainContentTab import MainContentTab
from GUI.repeatDetect.FormPanel import FormPanel
from GUI.repeatDetect.ResultPanel import ResultPanel


class MainContentTabCheck(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'repeatDetect')
        self.createFormAndResult(FormPanel, ResultPanel)