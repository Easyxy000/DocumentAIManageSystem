from GUI.main.MainContentTab import MainContentTab
from GUI.setting.FormPanel import FormPanel

class SettingTab(MainContentTab):
    def __init__(self, parent, size):
        super().__init__(parent, size, 'setting')
        self.createOnlyForm(FormPanel, size)
    def createOnlyForm(self, FormConstructor, size):
        # 获得尺寸
        w, h = size.width(), size.height()

        # 创建表单面板
        formPanel = FormConstructor(self)
        formPanel.resize(w, h)
        formPanel.show()


        # 赋予成员变量
        self.formPanel = formPanel

    def triggerFormPanel(self):
        pass
    def triggerResultPanel(self):
        pass