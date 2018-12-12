import hashlib, sys
import os
from copy import copy

from core.File import File


class RepeatFileSearch(File):
    def __init__(self, closeFields=None):
        super().__init__(closeFields)
    def search(self, path, exts=None):
        checkFirs = [path]
        fileAndSize = []
        while len(checkFirs) > 0:
            for root, dirs, files in os.walk(checkFirs.pop(), topdown=False):
                for file in files:
                    if file[0] == ".": continue
                    p = os.path.join(root, file)
                    s = file.rfind(".")
                    ext = file[s + 1 : ].lower()
                    if exts is not None and  ext not in exts: continue
                    try:
                        size = os.path.getsize(p)
                    except:
                        continue
                    fileAndSize.append((p, size))
                for dir in dirs:
                    checkFirs.append(dir)
        fileAndSize = sorted(fileAndSize, key=lambda x: x[1])
        fileEveryMd5 = {}
        i, l = 0, len(fileAndSize) - 1
        while i < l:
            if fileAndSize[i][1] != fileAndSize[i + 1][1]:
                i += 1
            else:
                size = fileAndSize[i][1]
                while i <= l and fileAndSize[i][1] == size:
                    item = fileAndSize[i]
                    md5 = self.createChecksum(item[0])
                    fileEveryMd5.setdefault(md5, [])
                    fileEveryMd5[md5].append(item[0])
                    i += 1
        results = []
        for key in fileEveryMd5:
            if len(fileEveryMd5[key]) > 1:
                completePaths = fileEveryMd5[key]
                group = []
                for completePath in completePaths:
                    fileData = self.buildData(completePath)
                    group.append(fileData)
                item = copy(group[0])
                item["children"] = group
                item["childrenCount"] = len(group)
                item["checked"] = 0

                results.append(item)
        return results
    def createChecksum(self, path):
        fp = open(path, "rb")
        checksum = hashlib.md5()
        while True:
            buffer = fp.read(8192)
            if not buffer: break
            checksum.update(buffer)
        fp.close()
        checksum = checksum.digest()
        return checksum