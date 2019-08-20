import hashlib

#md5，其实就是一种算法。可以将一个字符串，或文件，或压缩包，执行md5后，就可以生成一个固定长度为128bit的串。这个串，基本上是唯一的。

#加密明文
str = input("请输入要加密明文：")
hl = hashlib.md5()# 创建md5对象
hl.update(str.encode(encoding='utf-8'))# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing

if str:
    print('MD5加密前为：' + str)
    print('MD5加密后为：' + hl.hexdigest())#MD5加密后
input("Please Enter is Exit:")