import sys
import subprocess
import os

from PyQt5.QtWidgets import QPushButton

from configs.GUI import GUI_CONFIGS
from configs.form import FORM_CONFIGS
from configs.globalStyleSheet import GLOBAL_STYLE_SHEET
from configs.search import SEARCH_CONFIGS
from configs.configs import BASE_CONGIGS
from configs.UIElements import UI_ELEMENTS_CONFIG
import time
import getpass
from enum import Enum
configs = {
    "config" : BASE_CONGIGS,
    "gui" : GUI_CONFIGS,
    'search' : SEARCH_CONFIGS,
    'UIElements' : UI_ELEMENTS_CONFIG,
    "form" : FORM_CONFIGS,
    "globalStyleSheet" : GLOBAL_STYLE_SHEET
}

# 系统常量
SORT_ROOT = os.getcwd()

# 获得系统配置
def config(settingName):
    layres = settingName.split(".")
    if len(layres) == 1:
        return configs[layres[0]]
    return configs[layres[0]][layres[1]]

# 设置系统配置
def setConfig(settingName, val):
    layres = settingName.split(".")
    if len(layres) == 1:
        configs[layres[0]] = val
    configs[layres[0]][layres[1]] = val
root = None

# 设置系统变量
def initSystemVariable():
    configs["system"] = {
        "sortRoot" : SORT_ROOT
    }

# 获得缓存缩略图文件夹
def getThumbCacheDir(key):
    return os.path.join("cache/thumb", key)
# 获得用户根目录
def getUserRoot():
    global root
    if root is None:
        root = "/users/{0}".format(getpass.getuser())
    return root

# 将时间戳转化为标准格式
def timestampConvertToString(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

# 将文件尺寸转化为字节
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

# 打开文件
def openFile(file):
    platform = sys.platform
    if platform == "darwin":
        subprocess.call(["open",file])
    elif platform == "Windows":
        os.startfile(file)
    elif platform == "Linux":
        subprocess.call(["xdg-open", file])

initSystemVariable()

DEFAULT, PRIMARY, SUCCESS, INFO, WARNING, DANGER = range(6)
styleNames = ["default", "primary", "success", "info", "warning", "danger"]
def getBtn(style : int, text, parent=None):
    btn =  QPushButton(text, parent)
    btn.setObjectName("button_{0}".format(styleNames[style]))
    return btn