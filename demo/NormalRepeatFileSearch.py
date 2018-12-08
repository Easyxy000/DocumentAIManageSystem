import hashlib, sys
import os

class NormalRepeatFileSearch:
    def __init__(self):
        pass
    def search(self, path):
        checkFirs = [path]
        fileEveryMd5 = {}
        while len(checkFirs) > 0:
            for root, dirs, files in os.walk(checkFirs.pop(), topdown=False):
                for file in files:
                    p = os.path.join(root, file)
                    # print(p)
                    md5 = self.createChecksum(p)
                    fileEveryMd5.setdefault(md5, [])
                    fileEveryMd5[md5].append(p)
                for dir in dirs:
                    checkFirs.append(dir)
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