import requests
from bs4 import BeautifulSoup
import re
import pymysql
import psycopg2
import urllib.parse,urllib.request
import hashlib
import urllib
import random
import json
from translate import Translator

#百度翻译账号
appid = '20230220001568685'
secretKey = 'DoKaFuEaqW35mE7SW64P'
url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

#百度翻译
def translateBaidu(text, f='en', t='zh'):
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    url = url_baidu + '?appid=' + appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
        '&salt=' + str(salt) + '&sign=' + sign
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = json.loads(content)
    print(data)
    result = str(data['trans_result'][0]['dst'])
    print(result)
    return result

#创建表结构
def create():
    #mysql连接数据库
    #conn = pymysql.connect("localhost", "root", "root", "test")#连接数据库
    #postgresql链接数据库
    conn = psycopg2.connect(database="edw", user="gpadmin", password="gpadmin123", host="192.168.0.233", port="5432")
    cur = conn.cursor()
    cur.execute("drop table if exists t_fun_max")
    #mysql脚本
    #cur.execute("create table t_fun_max(id int primary key auto_increment,name varchar(200),grammar varchar(1000),describe1 varchar(1000));")
    #postgresql脚本
    cur.execute("create table t_fun_max(id serial primary key, name varchar,grammar varchar,describe1 varchar);")

    conn.commit()
    cur.close()
    conn.close()

#插入数据
def insert(value):
    #mysql连接数据库
    #conn = pymysql.connect("localhost", "root", "root", "test")#连接数据库
    #postgresql链接数据库
    conn = psycopg2.connect(database="edw", user="gpadmin", password="gpadmin123", host="192.168.0.233", port="5432")

    cur = conn.cursor()
    sql = "insert into t_fun_max(name,grammar,describe1) values(%s, %s, %s)"
    try:
        cur.execute(sql,value)
        conn.commit()
        print('插入数据成功')
    except Exception as e:
        conn.rollback()
        print(e)
        print("插入数据失败")
    conn.close()
#创建表
create()

#re匹配需要的数据
pertern = re.compile(r'<td style="text-align:left"><a href=".*?">(.*?)</a></td>.*?<td style="text-align:left">(.*?)</td>',re.S)
url = 'https://docs.dremio.com/software/sql-reference/sql-functions/ALL_FUNCTIONS/?parent=sql-functions'
res = requests.get(url)
res.encoding='utf-8'
#print(res.status_code)
soup = BeautifulSoup(res.text, 'html.parser')
data = soup.find_all('tbody')
data = str(data)
items = re.findall(pertern, data)
#获取第一层数据，钻取到第二层详情函数信息进行拼接插入数据库
for i,item in enumerate(items):
    #print(item)
    #通过第一层的链接地址拼接第二层链接地址获取函数的详情信息
    res = requests.get('https://docs.dremio.com/software/sql-reference/sql-functions/functions/'+item[0])
    res.encoding='utf-8'
    print(res.status_code)
    #因为该页面有多组标签数据，只获取第一组数据即可，通过正则表达进行过滤
    pertern = re.compile(r'<div id="body-inner">.*?<h3.*?>(.*?)</h3>.*?</div>[^\1]+',re.S)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.find_all('body')
    data = str(data)
    fun_text = re.findall(pertern, data)
    #获取语法元素
    for k,fitem in enumerate(fun_text):
        #翻译函数描述
        fun_des = translateBaidu(item[1])
        #获取参数的li元素
        li_list = soup.select('#body-inner ul')
        #非空判断
        if li_list:
            str_list = []
            for li in li_list[0].find_all('li'):
                #拼接语法和参数
                parameter = li.text.split(":")
                parameter_translation = translateBaidu(parameter[1])
                str_list.append('. '+parameter[0]+": "+parameter_translation)
                str_list.append('</br>')
        #拼接
        params = fitem.strip() + '</br>' + ''.join(str_list)
        print(fitem)
        #从新拼接参数
        v_item = (''+item[0].strip()+'',''+params+'',''+fun_des+'')
    #print(v_item)
    #调用插入数据方法
    insert(v_item)