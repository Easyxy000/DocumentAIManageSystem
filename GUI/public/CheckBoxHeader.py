from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtWidgets import QHeaderView, QStyleOptionButton, QStyle

from GUI.public import FileTableModel


class CheckBoxHeader(QHeaderView):
    clicked = pyqtSignal(bool)

    _x_offset = 3
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height()-self._width)/2.)

        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                model : FileTableModel = self.parent().model
                rowCount = self.parent().model.rowCount()
                model.beginResetModel()
                if self.isOn:
                    self.isOn = False
                    model.checkList = [False] * rowCount
                else:
                    self.isOn = True

                    model.checkList = [True] * rowCount
                model.endResetModel()
                self.clicked.emit(self.isOn)
                self.update()
        else:
            self.parent().model.sortByField(index - 1)
        super(CheckBoxHeader, self).mousePressEvent(event)