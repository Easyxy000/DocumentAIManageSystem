import time
def QdateConvertoTime(date):
    return time.mktime((date.year(), date.month(), date.day(), 0, 0, 0, date.dayOfWeek(), date.dayOfYear(), -1))
