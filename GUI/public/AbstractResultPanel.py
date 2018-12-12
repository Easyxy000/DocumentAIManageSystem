import math

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTableView, \
    QFrame, QAbstractItemView, QWidget, QGridLayout

from GUI.main.EventSystem import eventSystem
from GUI.public.CheckBoxHeader import CheckBoxHeader
from GUI.public.FileTableModel import FileTableModel
from core.Field import Field
from functions import fileSizeConvertToFitUnit, timestampConvertToString, getBtn, SUCCESS, WARNING, PRIMARY, DANGER, \
    DEFAULT
BUTTON_GROUP_MAX_COL = 6
BUTTON_GROUP_HEIGHT_EVERY_ROW = 45
class AbstractResultPanel(QWidget):

    def __init__(self, parent, size, specialFields=None, closeFields=None):
        super().__init__(parent)
        self.resize(*size)
        if closeFields is None: closeFields = []
        fields = self.createModel(specialFields, closeFields)

        btns = self._getBtns()
        row = math.ceil(len(btns) / BUTTON_GROUP_MAX_COL)
        col = math.ceil(len(btns) / row)
        btnGroupH = BUTTON_GROUP_HEIGHT_EVERY_ROW * row

        tableH = size[1] - btnGroupH
        self.tableView = self.createQTableView((size[0], tableH), fields)

        self._createBtnGroup(btns, (size[0], btnGroupH),(0, tableH), col)

        self.listenEvents()
    def createModel(self,specialFields, closeFields):
        if specialFields == None:
            specialFields = []
        fields = specialFields
        normalFields = [
                Field("fileName", "文件名", defaultSize=120),
                Field("fileSize", "文件大小", defaultSize=60,formatMethod=fileSizeConvertToFitUnit),
                Field("createdTime", "创建时间", defaultSize=160, formatMethod=timestampConvertToString),
                Field("updatedTime", "修改时间", defaultSize=160,formatMethod=timestampConvertToString),
                Field("accessTime", "最近一次访问时间", defaultSize=160, formatMethod=timestampConvertToString),
                Field("path", "所属目录",defaultSize=250)
            ]
        for field in normalFields:
            if field.id not in closeFields:
                fields.append(field)
        self.model = FileTableModel(fields)
        return fields
    def createQTableView(self, size, fields):
        model = self.model
        tableView = QTableView(self)
        tableView.setFrameShape(QFrame.NoFrame)
        tableView.setMinimumSize(*size)

        tableView.setModel(model)
        tableView.model = model
        tableView.setFrameShape(QFrame.NoFrame)
        tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = CheckBoxHeader()
        tableView.setHorizontalHeader(header)
        tableView.verticalHeader().setDefaultSectionSize(50)
        tableView.setColumnWidth(0, 30)

        for i, field in enumerate(fields):
            tableView.setColumnWidth(i + 1, field.defaultSize)
            if field.delegateClass is not None:
                tableView.setItemDelegateForColumn(i + 1, field.delegateClass(tableView, *field.delegateParameters))

        header = tableView.horizontalHeader()
        header.sectionClicked[int].connect(model.sortByField)

        model.tableView = tableView
        return tableView
    def listenEvents(self):
        pass
    def _getBtns(self):
        openChecked = getBtn(DEFAULT, "打开所选")
        openChecked.clicked.connect(self.model.openChecked)

        moveChecked = getBtn(WARNING,"移动所选")
        moveChecked.clicked.connect(self.model.moveChecked)

        deleteButton = getBtn(DANGER,"删除所选")
        deleteButton.clicked.connect(self.model.deleteChecked)

        return [openChecked, moveChecked, deleteButton] + self.getBtns()

    def _createBtnGroup(self, btns, size, movePos, colEveryRow):
        btnWidget = QWidget(self)
        btnWidget.resize(*size)
        btnWidget.move(*movePos)
        btnLayout = QGridLayout()
        row = 0
        col = 0
        for i, btn in enumerate(btns):
            if i % colEveryRow == 0:
                col = 0
                row += 1
            btnLayout.addWidget(btn, row, col)
            col += 1
        btnLayout.setSpacing(20)
        btnWidget.setLayout(btnLayout)