from GUI.classify.imageCluster.FormPanel import FormPanel
from GUI.classify.imageCluster.ResultPanel import ResultPanel
from GUI.main.MainContentTab import MainContentTab


class ImageClusterTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'ImageCluster')
        self.createFormAndResult(FormPanel, ResultPanel)