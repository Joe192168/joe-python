import re
import os
import time
import datetime
import random
import openpyxl
import sys
import traceback
import logging
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#获取当前时间
nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#组装exlce文件名称
_exclName = "yp" + nowTime + ".xlsx"
data_list= []#设置全局变量用来存储数据

#无界面 测试有问题暂时有问题
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')#非沙盒模式运行
#chrome_options.add_argument('--headless') #headless模式启动
chrome_options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument("--start-maximized") #最大化
chrome_options.add_argument('blink-settings=imagesEnabled=false')#不加载图片
chromeDriverPath = r'.\tools\chromedriver.exe'
browser = webdriver.Chrome()
wait =WebDriverWait(browser,50)#设置等待时间

#登陆
def login():
    print("*************要帮忙爬取数据操作界面***************")
    #用户名
    username = input("用户名：")
    #登录密码
    password = input("登录密码：")
    #爬虫网址
    browser.get('http://www.ybm100.com/login/login.htm')
    browser.find_element_by_xpath('//*[@id="inputPhone"]').send_keys('13368049626')
    browser.find_element_by_xpath('//*[@id="inputPassword"]').send_keys('qfgdyf100')
    browser.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div/button').click()

#页面加载计时器
def download_web(c_time):
    # 设置随机延迟
    for k in range(c_time,-1,-1):
        print('\r','距离页面数据加载结束还有 %s 秒！' % str(k).zfill(2),end='')
        time.sleep(1)
    print('\r','{:^20}'.format('页面加载结束！'))

#搜索
def search(keyword):
    try:
        mainhandle = browser.current_window_handle#主页面句柄  每个浏览器标签页都有一个句柄
        input = wait.until(
            EC.presence_of_all_elements_located((By.ID, 'search'))
        )
        #等到搜索框加载出来
        submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search-btn"]'))
        )
        #等到搜索按钮可以被点击
        #input[0].send_keys(keyword)#向搜索框内输入关键词
        browser.find_element_by_xpath('//*[@id="search"]').send_keys(keyword)
        submit.click()#点击
        #判断是否搜索到药品信息
        falg1 = isElementExist(browser,".mrth-new")
        if not falg1:
            print("没有搜索到该药品数据，关闭当前程序重新进行搜索！")
            #关闭浏览器
            browser.close()
        #browser.find_element_by_link_text("只看有货").click()#模拟用户点击
        # 通过css 找到type = checkbox
        #获取当前窗口句柄
        handles = browser.window_handles
        for handle in handles:# 轮流得出标签页的句柄 切换窗口
            if handle != mainhandle:
                browser.switch_to.window(handle)
        checkboxes = browser.find_elements_by_xpath("//*[@name='hasStock']//input[@type='checkbox']")
        if checkboxes:  # 判断是否有找到元素
            for checkbox in checkboxes:  # 循环点击找到的元素
                checkbox.click()  # 勾选复选框
        else:
            print("没有找到元素")
        #判断是否有分页元素存在
        falg2 = isElementExist(browser,".page")
        if falg2:
            total = wait.until(
                EC.presence_of_element_located((By.XPATH, './/.//div[@class="page"]//span'))
            )
            total = re.sub("\D", "", total.text)
            print("总共页数："+total)
        else :
            print("总共页数：1")
            total = 1#默认只有一页
        #滑动到底部，加载出商品信息
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait.until(
        #     EC.presence_of_all_elements_located((By.XPATH, './/div[@class="mrth-new"]'))
        # )
        #隐藏搜索浮动框
        #js_div = 'document.getElementsByClassName("followSearchPanel")[0].style="display: none;"'
        #browser.execute_script(js_div)
        html = browser.page_source#获取网页信息
        print("第", 1, "页：")
        # 设置计时器
        download_web(3)
        prase_html(html)#调用提取数据的函数
        #返回总页数
        return total
    except TimeoutError:
        print("请求超时，重新搜索该药品！。。。。。。。。")
        search()
    except Exception as e:
        print(e)
        #关闭浏览器
        browser.close()

#分页
def next_page(page_number):
    try:
        # 滑动到底部
        scroll_add_crowd_button = browser.find_element_by_xpath('.//div[@class="page"]')
        browser.execute_script("arguments[0].scrollIntoView();",scroll_add_crowd_button)
        time.sleep(random.randint(1, 3))#设置随机延迟
        # #隐藏搜索浮动框
        # js_div = 'document.getElementsByClassName("followSearchPanel")[0].style="display: none;"'
        # browser.execute_script(js_div)
        button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'next'))
        )#翻页按钮
        button.click()# 翻页动作
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="main"]//ul/li'))
        )#等到商品都加载出来
        # 滑动到底部，加载出后商品信息
        scroll_add_crowd_button = browser.find_element_by_xpath('.//div[@class="page"]')
        browser.execute_script("arguments[0].scrollIntoView();",scroll_add_crowd_button)
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="main"]//ul/li'))
        )#等到最后商品都加载出来
        #隐藏搜索浮动框
        # js_div = 'document.getElementsByClassName("followSearchPanel")[0].style="display: none;"'
        # browser.execute_script(js_div)
        # wait.until(
        #     EC.text_to_be_present_in_element((By.CLASS_NAME, "active"), str(page_number))
        # )# 判断翻页成功,高亮的按钮数字与设置的页码一样
        html = browser.page_source#获取网页信息
        # 设置计时器
        download_web(3)
        #调用提取数据的函数
        prase_html(html)
    except TimeoutError:
        return next_page(page_number)

#提取页面数据
def prase_html(html):
    # 开始提取信息,找到ul标签下的全部li标签
    try:
        ul = browser.find_elements_by_xpath('.//div[@class="main"]//ul[@class="mrth-new clearfix"]/li')
        # 遍历
        for li in ul:
            # 药品名称
            title = li.find_element_by_xpath('.//div[@class="row2"]//a').text
            # 售价 零售价 毛利
            row3 = li.find_element_by_xpath('.//div[@class="row3"]')
            # 药品公司名称
            li_ccompany = li.find_element_by_xpath('.//div[@class="row5 text-overflow"]').text
            if row3:
                li_price = row3.find_element_by_xpath('span')
                if li_price:
                    price = li_price.text
                else:
                    price = "商家尚未定价"
                row_last = row3.find_element_by_xpath('//div[@class="row-last"]')
                #零售价
                kongxiao_box = row_last.find_elements_by_xpath('//div[@class="kongxiao-box"]//span')
                if kongxiao_box:
                    retail_price = kongxiao_box[1].text
                else:
                    retail_price = ""
                maoli = row_last.find_elements_by_xpath('//div[@class="maoli-box"]//span')
                if maoli:
                    maoli = maoli[1].text
                else:
                    maoli = ""
            data_dict = []#写入字典
            data_dict.append(title)
            data_dict.append(price)
            data_dict.append(retail_price)
            data_dict.append(maoli)
            data_dict.append(li_ccompany)
            print(data_dict)
            data_list.append(data_dict)#写入全局变量
    except Exception as e:
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        # Get information about the exception that is currently being handled
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('e.message:\t', exc_value)
        print("Note, object e and exc of Class %s is %s the same." %
              (type(exc_value), ('not', '')[exc_value is e]))
        print('traceback.print_exc(): ', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())

#判断元素是否存在方法
def isElementExist(browser,css):
    try:
        browser.find_element_by_css_selector(css)
        return True
    except:
        return False

#新建excel
def creatwb(wbname):
    wb=openpyxl.Workbook()
    wb.save(filename=wbname)
    print ("新建Excel："+wbname+"成功")

#保存页面数据
def write_excel(fileName,d_list):
    wb = Workbook()
    #写入表头
    dilei_head = ['药品名称','售价','零售价','毛利','药品公司名称']
    sheet0Name = '药品数据信息'
    sheet0 = wb.create_sheet(sheet0Name, index=0)
    for i, item in enumerate(dilei_head):
        sheet0.cell(row = 1,column=i+1,value=item.encode('utf-8'))
    #写入数据
    for i, data in enumerate(d_list):
        for j, item in enumerate(data):
            sheet0.cell(row = i+2,column=j+1,value=item.encode('utf-8'))

    wb.save(fileName)
    print('excel文件写入完成')

#杀死浏览器进程
def kill_driver():
    #杀死这个chromedriver进程，因为每次启动都会打开，所以需要kill，这里用的chrome浏览器
    os.system('chcp 65001')
    os.system("taskkill /f /im chromedriver.exe")

#主方法
def main():
    #初始化exlce文件
    creatwb(_exclName)
    print("*************开始爬取有货药品数据请稍等***************")
    keyword = input("请输入要搜索药品名称：")#关键词
    total = int(search(keyword))
    # for i in range(2, 5):
    for i in range(2, total + 1):
        print("第", i, "页：")
        next_page(i)
    #保存数据到exlce中
    write_excel(_exclName,data_list)
    #关闭浏览器
    browser.close()

if __name__ == "__main__":
    #key_pass = input("请输入秘钥：")
    #校验秘钥 默认用123 md5加密
    #if key_pass=="202cb962ac59075b964b07152d234b70":
    #登陆
    login()
    #主方法入口
    main()
    # else :
    #     print("秘钥校验不正确，关闭该程序，重新运行！")
    #     #关闭浏览器
    #     browser.close()
    input("请按回车键退出！")
    #关闭浏览器进程
    kill_driver()