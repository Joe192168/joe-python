from selenium import webdriver
import requests

url = 'http://www.shanyaoo.com/_account/login.shtml'
driver = webdriver.Chrome()
#登录时没有验证码的情况下可以不打开浏览器，selenium
# option_chrome = webdriver.ChromeOptions()
# option_chrome.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=option_chrome)

driver.get(url)

driver.find_element_by_xpath('//input[@placeholder="用户名"]').send_keys('xs25391')
driver.find_element_by_xpath('//input[@placeholder="登录密码"]').send_keys('123456')
driver.find_element_by_xpath('//button[@class="loginBtn"]').click()

cookies = driver.get_cookies()
print(cookies)
cookies_list= []

for cookie_dict in cookies:
    cookie =cookie_dict['name']+'='+cookie_dict['value']
    cookies_list.append(cookie)

#print(cookies_list)

header_cookie = ';'.join(cookies_list)
#print(header_cookie)

headers = {
    'cookie':header_cookie,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

fin_url = 'http://www.shanyaoo.com/_shop/pazd/search.shtml?rt=ProductOfShop&sv=%E4%B8%AD%E8%8D%AF&total=691&ffs=&sn=2'
r = requests.get(fin_url,headers=headers)
print(r.text)