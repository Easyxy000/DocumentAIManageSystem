from functions import config
import time
class FormItem:
      def __init__(self, widget, getVal=None, id=None, col=1,row=1):
        self.widget = widget
        self.col = col
        self.id = id
        self.getVal = getVal
        self.row = row