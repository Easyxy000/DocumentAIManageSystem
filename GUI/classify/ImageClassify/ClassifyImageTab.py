from GUI.classify.ImageClassify.FormPanel import FormPanel
from GUI.classify.ImageClassify.ResultPanel import ResultPanel
from GUI.main.MainContentTab import MainContentTab


class ClassifyImageTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'imageClassify')
        self.createFormAndResult(FormPanel, ResultPanel)