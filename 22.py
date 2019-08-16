from selenium import webdriver
import requests






url = 'https://passport.lagou.com/login/login.html?ts=1534840857278&serviceId=lagou&service=https%253A%252F%252Fwww.lagou.com%252F&action=login&signature=7DF89D53F89F8440B1523001C02952DD'
driver = webdriver.Chrome()
#登录时没有验证码的情况下可以不打开浏览器，selenium
# option_chrome = webdriver.ChromeOptions()
# option_chrome.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=option_chrome)

driver.get(url)

driver.find_element_by_xpath('//input[@placeholder="请输入常用手机号/邮箱"]').send_keys('18601327484')
driver.find_element_by_xpath('//input[@placeholder="请输入密码"]').send_keys('15835791918ctDW')
driver.find_element_by_xpath('//input[@class="btn btn_green btn_active btn_block btn_lg"]').click()

cookies = driver.get_cookies()
print(cookies)
cookies_list= []

for cookie_dict in cookies:
    cookie =cookie_dict['name']+'='+cookie_dict['value']
    cookies_list.append(cookie)

print(cookies_list)

header_cookie = ';'.join(cookies_list)
print(header_cookie)

headers = {
    'cookie':header_cookie,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

fin_url = 'http://www.lagou.com'
response = requests.get(fin_url,headers=headers)

with open('lagou.html','wb') as f:
    f.write(response.content)