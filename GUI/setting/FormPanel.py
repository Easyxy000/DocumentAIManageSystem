from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, \
    QComboBox
from GUI.public.FormItem import FormItem
from GUI.public.AbstractFormPanel import AbstractFormPanel
from GUI.public.functions import config, PRIMARY, DEFAULT
from GUI.public.functions import getBtn
class FormPanel(AbstractFormPanel):
    def __init__(self, p):
        super().__init__(p)
        self.initUI("系统设置", bottomMargin=30)
    def createFieldGroup(self):
        self.createGroup(self.createAutoRunGroup, "启动设置", 'fileType')
        self.createGroup(self.createCacheLimit, "缓存设置", "cache")
        self.createGroup(self.createThumbSizes, "缩略图尺寸设置", "thumbCache")
        self.createGroup(self.createRootDirctoryChoose, "文件搜索默认目录", 'normalSearchDefaultDir')
        self.createGroup(self.createRootDirctoryChoose, "相似图像搜索默认目录", 'similarSearchDefaultDir')
        self.createGroup(self.createRootDirctoryChoose, "文本整理默认目录", 'textTidyDefaultDir')
        self.createGroup(self.createRootDirctoryChoose, "图像整理默认目录", 'imageTidyDefaultDir')
        self.createGroup(self.createRootDirctoryChoose, "碎片文件默认目录", 'dirtyFileDir')
    def createAutoRunGroup(self):
        cb = QCheckBox("是否开机启动", self)
        return FormItem(cb, getVal=cb.isChecked)
    def createCacheLimit(self):
        cb = QCheckBox("是否开启缓存", self)
        cacheLimit = QLineEdit(self)
        unit = QComboBox(self)
        self.addItemsFromData(unit, dict([(item, item) for item in config("search.units")]))
        return (
            FormItem(cb, getVal=cb.isChecked, id="onCache"),
            FormItem(QLabel("最大缓存空间", self)),
            FormItem(cacheLimit, getVal=cacheLimit.text, id="cacheLimit"),
            FormItem(unit, getVal=unit.currentData, id="cacheLimitUnit")
        )
    def createThumbSizes(self):
        w = QLineEdit(self)
        h = QLineEdit(self)
        return (
            FormItem(QLabel("宽", self)),
            FormItem(w, getVal=w.text, id="thumbW"),
            FormItem(QLabel("像素", self)),
            FormItem(QLabel("高", self)),
            FormItem(h, getVal=h.text, id="thumbH"),
            FormItem(QLabel("像素", self)),
        )
    def getBtns(self):
        submitButton = getBtn(PRIMARY, "提交", self)
        submitButton.clicked.connect(self.submit)
        resetButton = getBtn(DEFAULT, "重置", self)

        self.submitButton = submitButton
        return (submitButton,  resetButton)
    def submit(self):
        pass
