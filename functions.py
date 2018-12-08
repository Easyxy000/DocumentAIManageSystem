import sys

import subprocess

import os

from configs.GUI import GUI_CONFIGS
from configs.form import FORM_CONFIGS
from configs.globalStyleSheet import GLOBAL_STYLE_SHEET
from configs.search import SEARCH_CONFIGS
from configs.configs import BASE_CONGIGS
from configs.UIElements import UI_ELEMENTS_CONFIG
import time
import getpass
configs = {
    "config" : BASE_CONGIGS,
    "gui" : GUI_CONFIGS,
    'search' : SEARCH_CONFIGS,
    'UIElements' : UI_ELEMENTS_CONFIG,
    "form" : FORM_CONFIGS,
    "globalStyleSheet" : GLOBAL_STYLE_SHEET
}
def config(settingName):
    layres = settingName.split(".")
    if len(layres) == 1:
        return configs[layres[0]]
    return configs[layres[0]][layres[1]]

root = None
def getUserRoot():
    global root
    if root is None:
        root = "/users/{0}".format(getpass.getuser())
    return root
def timestampConvertToString(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
def fileSizeConvertToFitUnit(bitSize):
    if bitSize <= 0: return "--"
    if type(bitSize) != int:
        return "未知"
    units = SEARCH_CONFIGS["units"]
    i = 0
    while bitSize > 1024:
        bitSize /= 1024
        i += 1
    return str(int(bitSize)) + units[i]

def openFile(file):
    platform = sys.platform
    if platform == "darwin":
        subprocess.call(["open",file])
    elif platform == "Windows":
        os.startfile(file)
    elif platform == "Linux":
        subprocess.call(["xdg-open", file])