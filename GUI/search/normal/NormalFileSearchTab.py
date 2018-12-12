from GUI.main.MainContentTab import MainContentTab
from GUI.search.normal.FormPanel import FormPanel
from GUI.search.normal.ResultPanel import ResultPanel

class NormalFileSearchTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'normalSearch')
        self.createFormAndResult(FormPanel, ResultPanel)
