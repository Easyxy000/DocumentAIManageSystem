from time import time

from core.RepeatFileSearch import RepeatFileSearch

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