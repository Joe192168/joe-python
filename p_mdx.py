import requests
from bs4 import BeautifulSoup
import re
import pymysql
import psycopg2

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

create()  #创建表

#re匹配需要的数据
pertern = re.compile(r'<a data-linktype="relative-path" href="(.*?)">(.*?)</a>.*?<td>(.*?)</td>',re.S)
url = 'https://docs.microsoft.com/zh-cn/sql/mdx/mdx-function-reference-mdx?view=sql-server-2017'
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
    res = requests.get('https://learn.microsoft.com/zh-cn/sql/mdx/'+item[0])
    res.encoding='utf-8'
    print(res.status_code)
    #因为该页面有多组标签数据，只获取第一组数据即可，通过正则表达进行过滤
    pertern = re.compile(r'<pre.*?><code.*?>(.*?)</code></pre>[^\1]+',re.S)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.find_all('main')
    data = str(data)
    fun_text = re.findall(pertern, data)
    for k,fitem in enumerate(fun_text):
        print(fitem)
        #从新拼接参数
        v_item = (''+item[1].strip()+'',''+fitem.strip().replace(',','').replace('\n','')+'',''+item[2]+'')
        #print(v_item)
        #调用插入数据方法
        insert(v_item)