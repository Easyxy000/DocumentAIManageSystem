import os

from core.File import File


class FileSearcher(File):
    def __init__(self):
        super().__init__(None)
    def search(self):
        self.researchInit()
        results = []
        self.lastResult = results
        addDir = not self.hasFileSizeFilter and not self.hasExtensionFilter
        for root, dirs, files in os.walk(self.path, topdown=False):
            if root[0] == ".": continue
            if addDir:
                e = root.rfind("/")
                fileData = self.filterAndBuildData(root[e+1:], root[:e], True)
                if fileData is not None:
                    yield fileData
                    results.append(fileData)
            for file in files:
                if file[0] == ".": continue
                fileData = self.filterAndBuildData(file, root)
                if fileData is not None:
                    yield fileData
                    results.append(fileData)
        self.stopSearch()
    def setPath(self, path):
        self.path = path
    def filterItems(self, items):
        result = []
        for item in items:
            if self.filter(item):
                result.append(item)
        return result


