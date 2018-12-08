import os
class FileSearcher:
    def __init__(self):

        self.fieldGetter = {
            "fileSize" : lambda fileName : os.path.getsize(fileName),
            "createdTime" : lambda fileName : os.path.getctime(fileName),
            "updatedTime" : lambda fileName : os.path.getmtime(fileName),
            "accessTime": lambda fileName: os.path.getmtime(fileName),
        }
        self.otherAttr = []
        self.filterInit()
        self.lastResult = None
    def filterInit(self):
        self.hasExtensionFilter = False
        self.hasFileSizeFilter = False
        self.fileNameFilters = []
        self.filters = {}
    def researchInit(self):
        attrs = self.fieldGetter.keys()
        filterAttrs = self.filters.keys()
        for attr in attrs:
            if attr not in filterAttrs:
                self.otherAttr.append(attr)
        self.lastResult = None
    def search(self, path):
        self.researchInit()
        results = []
        self.lastResult = results
        addDir = not self.hasFileSizeFilter and not self.hasExtensionFilter
        for root, dirs, files in os.walk(path, topdown=False):
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
    def stopSearch(self):
        self.filterInit()
    def filterInResults(self):
        if self.lastResult == None:
            return []
        results = []
        for item in self.lastResult:
            if self.filter(item) == True:
                results.append(item)
        return results
    def filter(self, item):
        for filter in self.fileNameFilters:
            if not filter(item["fileName"]): return False
        for field in self.filters:
            for filter in self.filters[field]:
                if not filter(item[field]): return False

        return True
    def filterAndBuildData(self, fileName, path, isDir=False):
        for filter in self.fileNameFilters:
            if filter(fileName) == False:return None
        fileData = {}
        completePath = os.path.join(path, fileName)
        for field in self.filters:
            try:
                val = self.fieldGetter[field](completePath)
            except:
                val = None
            for filter in self.filters[field]:
                if filter(val) == False: return None
            fileData[field] = val
        for field in self.otherAttr:
            try:
                fileData[field] = self.fieldGetter[field](completePath)
            except:
                fileData[field] = None
        fileData["fileName"] = fileName
        fileData["path"] = path
        if isDir:
            fileData["fileSize"] = -1
        return fileData
    def setKeywordFilter(self, keywords, containAll=True):
        if containAll:
            def filter(fileName):
                for keyword in keywords:
                    if keyword not in fileName:
                         return False
                return True
        else:
            def filter(fileName):
                for keyword in keywords:
                    if keyword in fileName:
                         return True
                return False
        self._addFilter("fileName",filter)
    def setExtensionFilter(self, exts):
        self.hasExtensionFilter = True
        def filter(fileName):
            fileExt = fileName.split(".")[-1].lower()
            for ext in exts:
                if fileExt == ext: return True
            return False
        self._addFilter('fileName',filter)
    def _addFilter(self, field, filter):
        if field == "fileName":
            self.fileNameFilters.append(filter)
            return
        self.filters.setdefault(field, [])
        self.filters[field].append(filter)
    def setFileSizeFilter(self, min=None, max=None):
        self.hasFileSizeFilter = True
        self._setBetweenFilter("fileSize", min, max)
    def setCreatedTimeFilter(self, start=None, end=None):
        self._setBetweenFilter("createdTime", start, end)
    def setUpdatedTimeFilter(self, start, end):
        self._setBetweenFilter("updatedTime", start, end)
    def setAccessTimeFilter(self, start, end):
        self._setBetweenFilter("accessTime", start, end)
    def _setBetweenFilter(self,field, min=None, max=None):
        if min is not None:
            def minFilter(fileSize):
                return fileSize >= min
            self._addFilter(field, minFilter)
        if max is not None:
            def maxFilter(fileSize):
                return fileSize <= max
            self._addFilter(field, maxFilter)
