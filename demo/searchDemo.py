from core.FileSearch import FileSearcher
searcher = FileSearcher()
searcher.setKeywordFilter(["你", "我"],containAll=False)
# searcher.setFileSizeFilter(min=750000, max=800000)
# searcher.setExtensionFilter(["jpg","png"])
for item in searcher.search("/users/xushaojun/Documents/吉他谱"):
    # print(item)
    print("{0}\t{1}".format(item["fileName"], item["createdTime"]))


print("\n\nfilter in results:")
searcher.setKeywordFilter(["你", "我"],containAll=True)
for item in searcher.filterInResults():
    print(item["fileName"])
# import  os
# dir_path = "/users/xushaojun/Documents/吉他谱"
# for root, dirs, files in os.walk(dir_path):
#     for filename in files:
#         print("file:%s\n" % filename)
#     for dirname in dirs:
#         print("dir:%s\n" % dirname)
#     print("")
