from GUI.classify.textClassify.FormPanel import FormPanel
from GUI.classify.textClassify.ResultPanel import ResultPanel
from GUI.main.MainContentTab import MainContentTab


class ClassifyTextTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'textClassify')
        self.createFormAndResult(FormPanel, ResultPanel)