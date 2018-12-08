from PyQt5.QtWidgets import QLabel, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QFileDialog
from PyQt5.Qt import Qt

from GUI.MainContentTab import MainContentTab
from functions import config, getUserRoot
from GUI.components.FormItem import FormItem
import time
class FormTable(QLabel):
    units = config("search.units")
    def __init__(self, p : MainContentTab):
        super().__init__(p)
        self.p = p
    def unitFormat(self, val, unit):
        if val == "": return None
        return int(val) ** (FormTable.units.index(unit) + 1)
    def QdateConvertoTime(self, date):
        if date == None: return None
        return time.mktime((date.year(), date.month(), date.day(), 0, 0, 0, date.dayOfWeek(), date.dayOfYear(), -1))
    def createGroup(self, builder, groupName, gorupId, col=None, *args):
        self.form.setdefault(gorupId, {})
        label = QLabel(self)
        label.setText(groupName + "：")
        label.setAlignment(Qt.AlignRight)
        self.grid.addWidget(label, self.row, 0)

        widgets = builder(*args)

        if col == None:
            col = sum([item.col for item in widgets]) if type(widgets) == tuple else widgets.col

        grid = QGridLayout()
        c = 0
        r = 0

        if(type(widgets) == tuple or type(widgets) == list):
            maxRow = 1
            for i in range(len(widgets)):
                item = widgets[i]
                if i > 0 and c % col == 0 :
                    c = 0
                    r += maxRow
                    maxRow = 1
                grid.addWidget(item.widget, r, c, item.row, item.col)
                if item.row > maxRow: maxRow = item.row
                c += item.col
                if item.getVal == None: continue
                if item.id == None:
                    self.form[gorupId] = item
                else:
                    self.form[gorupId][item.id] = item
        else:
            grid.addWidget(widgets.widget, 0, 1)
            self.form[gorupId] = widgets
        self.grid.addLayout(grid, self.row, 1)
        self.row += 1
    def getForm(self):
        data = {}
        for key in self.form:
            if key == "buttons": continue
            row = self.form[key]
            if(type(row) == dict):
                group = {}
                for name in row:
                    group[name] = row[name].getVal()
            else:
                group = row.getVal()
            data[key] = group
        for key in data:
            print("{0}:".format(key))
            print(data[key])
        return data
    def createRootDirctoryChoose(self, type="dirctory"):
        textEdit = QLineEdit(self)
        textEdit.setText(getUserRoot())
        btn = QPushButton("浏览", self)
        btn.setObjectName("fileChooseBtn")
        btn.clicked.connect(self.getChooseRootDirctory(textEdit, type))
        return (FormItem(textEdit, getVal=textEdit.text, col=1),FormItem(btn, col=4))
    def getChooseRootDirctory(self, lineEdit, type):
        def event():
            if type == "dirctory":
                fname = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
            else:
                fname = QFileDialog.getOpenFileUrl(self, 'Open file', '/home')[0].path()
            print(fname)
            if fname == "": return
            lineEdit.setText(fname)
        return event
    def _createButtonGroup(self, buttonGroupLayout):
        self.grid.addLayout(buttonGroupLayout,self.row, 0, 1, 2)
