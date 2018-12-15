from time import time
import hashlib, sys
import os
from copy import copy
from zipfile import ZipFile
from core.File import File

zipExts = ["zip", "rar"]
class RepeatFileSearch(File):
    def __init__(self, closeFields=None):
        super().__init__(closeFields)
    def search(self, path, exts=None):
        checkFirs = [path]
        fileAndSize = []
        zipFiles = []
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
                    fileAndSize.append((p, size, False))

                    if ext in zipExts:
                        zipFiles.append(p)
                for dir in dirs:
                    checkFirs.append(dir)
        # for zipPath in zipFiles:
        #     zip = ZipFile(zipPath)
        #     for item in zip.namelist():
        #         if item[0] == ".": continue
        #         if item[-1] == "/": continue
        #         if "__MACOSX" in item: continue
        #         if ".DS_Store" in item: continue
        #         formatName = item.encode('cp437').decode('utf-8')
        #         fileAndSize.append((os.path.join(zipPath, formatName), zip.getinfo(item), True))
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
root = "/users/xushaojun/Documents/数学建模"
exts = ["png","jpg","pdf"]
searcher = RepeatFileSearch()
start = time()
results = searcher.search(root)
index = 1
for group in results:
    print("\ngroup {0} has {1}:".format(index, group["childrenCount"]))
    index += 1
    for item in group["children"]:
        print(item)
print("cost:{0}\n\n\n".format(time() - start))

removePaths = []
for group in results:
    group["children"] = sorted(group["children"], key=lambda x : x["createdTime"])
    removePaths += [os.path.join(item["path"], item["fileName"]) for item in group["children"][1:]]

print("remove {0} items ,left".format(len(removePaths)), sum([len(group["children"]) for group in results]) - len(removePaths))
for item in removePaths:
    print("remove {0}".format(item))
#test repeat in zip:
#import zipfile, os
#zip = zipfile.ZipFile("/users/xushaojun/Documents/吉他谱/遇见.jpg.zip")
#zip.namelist()
#['ΘüçΦºü.jpg', '__MACOSX/', '__MACOSX/._ΘüçΦºü.jpg']
#zip.getinfo("ΘüçΦºü.jpg")
#fp = zip.open("ΘüçΦºü.jpg")
# checksum = hashlib.md5()
# while True:
#     buffer = fp.read(8192)
#     if not buffer: break
#     checksum.update(buffer)
# fp.close()
# checksum = checksum.digest()