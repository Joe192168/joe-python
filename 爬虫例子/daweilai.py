import requests
from lxml import etree
import json
url_1 = 'http://www.daweilai211.com/Account/Login'
headers = {
    'Referer': 'http://www.daweilai211.com/account/Login',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
}

# 获取验证码到本地
html = requests.get(url_1,headers=headers).text
tree_login = etree.HTML(html)
# 获取验证码地址
img_test = tree_login.xpath('/html/body/div[3]/div/div/div/div/form/table/tbody/tr[5]/td[3]/div/img/@src')[0]
img_link = 'http://www.daweilai211.com' + img_test
# 下载该验证码
img = requests.get(img_link,headers=headers).content
with open('./验证码.gif','wb') as fp:
    fp.write(img)
    print('验证码已下载完毕')

code = int(input('请输入得到的验证码：') )
# 找到post的url和之前相同
# 先创建一个session对象来收集cookie
# 输入post的数据
data = {
    'username': 'YN170146',
    'password': '276524',
    'CheckCode': code
}
session = requests.Session()
url_login = session.post(url_1,headers=headers,data=data)


# 主页：
url_info_scores = 'http://www.daweilai211.com/fangan20/index'
info = session.get(url_info_scores)
info_text = info.text
with open('test.html','w',encoding='utf-8') as fp:
    fp.write(info_text)

