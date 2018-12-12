from GUI.classify.textCluster.FormPanel import FormPanel
from GUI.classify.textCluster.ResultPanel import ResultPanel
from GUI.main.MainContentTab import MainContentTab


class ClusterTextTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'textCluster')
        self.createFormAndResult(FormPanel, ResultPanel)