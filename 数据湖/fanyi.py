import re
import urllib.parse,urllib.request
import hashlib
import urllib
import random
import json
import time
from translate import Translator

appid = '20210203000689585'
secretKey = 'kqD9YO_jFfvjCmplPHDv'
url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'


#字段名	类型	必填参数	描述	备注
#q	TEXT	Y	请求翻译query	UTF-8编码
#from	TEXT	Y	翻译源语言	语言列表(可设置为auto)
#to	TEXT	Y	译文语言	语言列表(不可设置为auto)
#appid	INT	Y	APP ID	可在管理控制台查看
#salt	INT	Y	随机数	
#sign	TEXT	Y	签名	appid+q+salt+密钥 的MD5值


#字段名	类型	必填参数	描述	备注
#q	TEXT	Y	请求翻译query	UTF-8编码
#from	TEXT	Y	翻译源语言	语言列表(可设置为auto)
#to	TEXT	Y	译文语言	语言列表(不可设置为auto)
#appid	INT	Y	APP ID	可在管理控制台查看
#salt	INT	Y	随机数	
#sign	TEXT	Y	签名	appid+q+salt+密钥 的MD5值
 
def translateBaidu(text, f='en', t='zh'):
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    url = url_baidu + '?appid=' + appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
        '&salt=' + str(salt) + '&sign=' + sign
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = json.loads(content)
    result = str(data['trans_result'][0]['dst'])
    print(result)

text_list = ['Returns the approximate number of rows that contain distinct values in a column. Ignores rows that contain a null value for the column.']

time_baidu = 0

for text in text_list:
    time1 = time.time()
    translateBaidu(text)
    time2 = time.time()
    time_baidu += (time2 - time1)

    print('百度翻译时间：%s' % (time_baidu / 10))