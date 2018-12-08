from functions import config
import time
class FormItem:
      def __init__(self, widget, getVal=None, id=None, col=1,row=1):
        # self.formaters = {
        #     "date": self.QdateConvertoTime,
        # }
        self.widget = widget
        self.col = col
        self.id = id
        self.getVal = getVal
        self.row = row
        # self.formater = self.formaters[formater] if type(formater) == str else None
    # def getVal(self):

        # if self.formater == None:
        #     return self.getRawVal()
        # else:
        #     return self.formater(self.getRawVal())