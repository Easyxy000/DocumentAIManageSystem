
from GUI.main.MainContentTab import MainContentTab
from GUI.search.similar.FormPanel import FormPanel
from GUI.search.similar.ResultPanel import ResultPanel
class SimilarImageSearchTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'similarImageSearch')
        self.createFormAndResult(FormPanel, ResultPanel)

