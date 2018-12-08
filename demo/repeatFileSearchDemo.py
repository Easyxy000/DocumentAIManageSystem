
from demo.NormalRepeatFileSearch import NormalRepeatFileSearch
from time import time

from demo.RepeatFileSearchByFileSize import RepeatFileSearchByFileSize
# test root:"/users/xushaojun/Documents/吉他谱"
# NormalRepeatFileSearch: cost:0.16192102432250977
# RepeatFileSearchByFileSize: cost:0.012562990188598633
from demo.RepeatFileSearchByFileSizeAndExt import RepeatFileSearchByFileSizeAndExt

root = "/users/xushaojun/Documents/数学建模"
exts = ["png","jpg","pdf"]
# searcher = NormalRepeatFileSearch()
# start = time()
# results = searcher.search(root)
# index = 1
# for group in results:
#     print("\ngroup {0}:".format(index))
#     index += 1
#     for item in group:
#         print(item)
# print("cost:{0}\n\n\n".format(time() - start))

searcher2 = RepeatFileSearchByFileSize()
start = time()
results = searcher2.search(root, exts)
index = 1
if False:
    for group in results:
        print("\ngroup {0}:".format(index))
        index += 1
        for item in group:
            print(item)
print("cost:{0}".format(time() - start))

searcher3 = RepeatFileSearchByFileSizeAndExt()
start = time()
results = searcher3.search(root, exts)
index = 1
if False:
    for group in results:
        print("\ngroup {0}:".format(index))
        index += 1
        for item in group:
            print(item)
print("cost:{0}".format(time() - start))


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