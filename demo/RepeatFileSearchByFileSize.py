import hashlib, sys
import os

class RepeatFileSearchByFileSize:
    def __init__(self):
        pass
    def search(self, path, exts=None):
        checkFirs = [path]
        fileAndSize = []
        s, ext = None, None

        while len(checkFirs) > 0:
            for root, dirs, files in os.walk(checkFirs.pop(), topdown=False):
                for file in files:
                    p = os.path.join(root, file)
                    s = file.rfind(".")
                    ext = file[s + 1 : ].lower()
                    if exts is not None and  ext not in exts: continue
                    fileAndSize.append((p, os.path.getsize(p)))
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
                results.append(fileEveryMd5[key])
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