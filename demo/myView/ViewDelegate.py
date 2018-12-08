from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QItemDelegate, QLabel


class ViewDelegate(QItemDelegate):
    def __init__(self, parent, fields):
        super(ViewDelegate, self).__init__(parent)
        self.fields = fields
        self.parentTarget = parent
        self.initFieldDelegates()
    def initFieldDelegates(self):
        delegates = []
        for field in self.fields:
            delegates.append(field.delegateClass(self.parentTarget) if field.delegateClass is not None else None)
        self.delegates = delegates

    def paint(self, painter, option, index):
        delegate = self.delegates[index.column()]
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            self.parent().setIndexWidget(
                index,
                QLabel(index.model().data(index))
            )
            # QItemDelegate.paint(self, painter, option, index)


    def sizeHint(self, option, index):
        delegate = self.delegates[index.column()]
        if delegate is not None:
            return delegate.sizeHint(option, index)
        else:
            return QItemDelegate.sizeHint(self, option, index)


    def createEditor(self, parent, option, index):
        delegate = self.delegates[index.column()]
        if delegate is not None:
            delegate.createEditor(parent, option,index)
        else:
            return QItemDelegate.createEditor(self, parent, option,index)
    #
    #
    # def commitAndCloseEditor(self):
    #     editor = self.sender()
    #     if isinstance(editor, (QTextEdit, QLineEdit)):
    #         self.emit(SIGNAL("commitData(QWidget*)"), editor)
    #         self.emit(SIGNAL("closeEditor(QWidget*)"), editor)
    #
    #
    # def setEditorData(self, editor, index):
    #     text = index.model().data(index, Qt.DisplayRole).toString()
    #     if index.column() == TEU:
    #         value = text.replace(QRegExp("[., ]"), "").toInt()[0]
    #         editor.setValue(value)
    #     elif index.column() in (OWNER, COUNTRY):
    #         i = editor.findText(text)
    #         if i == -1:
    #             i = 0
    #         editor.setCurrentIndex(i)
    #     elif index.column() == NAME:
    #         editor.setText(text)
    #     elif index.column() == DESCRIPTION:
    #         editor.setHtml(text)
    #     else:
    #         QItemDelegate.setEditorData(self, editor, index)
    #
    #
    # def setModelData(self, editor, model, index):
    #     QItemDelegate.setModelData(self, editor, model, index)