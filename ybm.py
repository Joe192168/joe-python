import re
import os
import time
import datetime
import random
import openpyxl
import sys
import traceback
from time import sleep
from openpyxl import Workbook
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

# 获取当前时间
nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# 设置全局变量用来存储数据
data_list = []
# 设置商品品种数组
data_varieties = []

# 无界面 测试有问题暂时有问题
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')#非沙盒模式运行
# chrome_options.add_argument('--headless') #headless模式启动
# chrome_options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument("--start-maximized") #最大化
# chrome_options.add_argument('blink-settings=imagesEnabled=false')#不加载图片
# chromeDriverPath = r'.\tools\chromedriver.exe'
browser = webdriver.Chrome()
# 设置等待时间
wait = WebDriverWait(browser, 50)

# 登陆
def login():
    print("*************要帮忙爬取数据操作界面***************")
    # 用户名
    username = input("用户名：")
    # 登录密码
    password = input("登录密码：")
    # 爬虫网址
    try:
        # 页面窗口最大化
        browser.maximize_window()
        browser.get('http://www.ybm100.com/login/login.htm')
        browser.find_element_by_xpath('//*[@id="inputPhone"]').send_keys('13368049626')
        browser.find_element_by_xpath('//*[@id="inputPassword"]').send_keys('qfgdyf100')
        browser.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div/button').click()
    except TimeoutException:
        print(u'页面加载超过设定时间，超时')
        # 当页面加载时间超过设定时间，
        browser.close()

# 页面加载计时器
def download_web(c_time):
    # 设置随机延迟
    for k in range(c_time,-1,-1):
        print('\r','页面加载倒计时，还有 %s 秒！请稍等。。。' % str(k).zfill(2),end='')
        time.sleep(1)
    print('\r','{:^20}'.format('页面加载完毕！'))

# 搜索
def search(keyword):
    try:
        # 主页面句柄  每个浏览器标签页都有一个句柄
        mainhandle = browser.current_window_handle
        # 等到搜索框加载出来
        submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search-btn"]'))
        )
        # 等到搜索按钮可以被点击
        browser.find_element_by_xpath('//*[@id="search"]').send_keys(keyword)
        submit.click()#点击
        # 判断是否搜索到药品信息
        falg1 = browser.find_element_by_xpath('/html/body/div[2]/div[5]').text
        if falg1 in "抱歉，没有找到商品":
            print("没有搜索到该药品数据，关闭当前程序重新进行搜索！")
            #关闭浏览器
            browser.close()
        # browser.find_element_by_link_text("只看有货").click()#模拟用户点击
        # 通过css 找到type = checkbox
        # 获取当前窗口句柄
        handles = browser.window_handles
        # 轮流得出标签页的句柄 切换窗口
        for handle in handles:
            if handle != mainhandle:
                browser.switch_to.window(handle)
        checkboxes = browser.find_elements_by_xpath("//*[@name='hasStock']//input[@type='checkbox']")
        if checkboxes:  # 判断是否有找到元素
            for checkbox in checkboxes:  # 循环点击找到的元素
                checkbox.click()  # 勾选复选框
        else:
            print("没有找到元素")
        # 判断是否有分页元素存在
        falg2 = isElementExist(browser,".page")
        if falg2:
            total = wait.until(
                EC.presence_of_element_located((By.XPATH, './/.//div[@class="page"]/div/div/span'))
            )
            total = re.sub("\D", "", total.text)
            print("总共页数："+total)
        else:
            print("总共页数：1")
            # 默认只有一页
            total = 1
        # 滑动到底部，加载出商品信息
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait.until(
        #     EC.presence_of_all_elements_located((By.XPATH, './/div[@class="mrth-new"]'))
        # )
        # 隐藏搜索浮动框
        # js_div = 'document.getElementsByClassName("followSearchPanel")[0].style="display: none;"'
        # browser.execute_script(js_div)
        # 获取网页信息
        html = browser.page_source
        print("第", 1, "页：")
        # 设置计时器
        download_web(3)
        # 总页数转换int
        total = int(total)
        # 调用提取数据的函数
        prase_html(html)
        # 返回总页数
        return total
    except TimeoutError:
        print("请求超时，重新搜索该药品！。。。。。。。。")
        search()
    except Exception as e:
        print(e)
        # 关闭浏览器
        browser.close()

# 模拟A标签点击搜索
def click_a(a_text):
    try:
        # 获取本网站商品品种
        ul = browser.find_elements_by_xpath('//*[@class="leimu-TC"]/ul[@class="two-box-ul"]/li')
        for li in ul:
            _li = li.find_elements_by_xpath('.//div[@class="hangbox"]/div[@class="hang-col1"]/div[@class="com-info"]/a')
            for _a in _li:
                if a_text == _a.get_attribute('text'):
                    _a.click()

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

# 分页
def next_page(page_number):
    try:
        # 滑动到底部
        scroll_add_crowd_button = browser.find_element_by_xpath('.//div[@class="page"]')
        browser.execute_script("arguments[0].scrollIntoView();",scroll_add_crowd_button)
        falg1 = browser.find_element_by_xpath('/html/body/div[2]/div[5]').text
        if falg1 in "抱歉，没有找到商品":
            print("没有搜索到该药品数据，继续下一页！")
            next_page(page_number+1)
        # 设置随机延迟
        time.sleep(random.randint(1, 3))
        # # 隐藏搜索浮动框
        # js_div = 'document.getElementsByClassName("followSearchPanel")[0].style="display: none;"'
        # browser.execute_script(js_div)
        button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'next'))
        )
        # 翻页按钮
        button.click()
        # 翻页动作
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="main"]//ul/li'))
        )
        # 等到商品都加载出来
        # 滑动到底部，加载出后商品信息
        scroll_add_crowd_button = browser.find_element_by_xpath('.//div[@class="page"]')
        browser.execute_script("arguments[0].scrollIntoView();",scroll_add_crowd_button)
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="main"]//ul/li'))
        )
        # 等到最后商品都加载出来
        # 隐藏搜索浮动框
        # js_div = 'document.getElementsByClassName("followSearchPanel")[0].style="display: none;"'
        # browser.execute_script(js_div)
        # wait.until(
        #     EC.text_to_be_present_in_element((By.CLASS_NAME, "active"), str(page_number))
        # )# 判断翻页成功,高亮的按钮数字与设置的页码一样
        # 获取网页信息
        html = browser.page_source
        # 设置计时器
        download_web(3)
        # 调用提取数据的函数
        prase_html(html)
    except TimeoutError:
        return next_page(page_number)

# 提取页面数据
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
            # 药品生成商
            ccompany = li.find_element_by_xpath('.//div[@class="row5 text-overflow"]').text
            # 药品供应商
            gys = li.find_element_by_xpath('.//div[@class="row7"]//a').text
            if row3:
                li_price = row3.find_element_by_xpath('span')
                if li_price:
                    price = li_price.text
                else:
                    price = "商家尚未定价"
                row_last = row3.find_element_by_xpath('//div[@class="row-last"]')
                # 零售价
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
            # 写入字典
            data_dict = []
            data_dict.append(title)
            data_dict.append(price)
            data_dict.append(retail_price)
            data_dict.append(maoli)
            data_dict.append(ccompany)
            data_dict.append(gys)
            print(data_dict)
            # 写入全局变量
            data_list.append(data_dict)
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

# 判断元素是否存在方法
def isElementExist(browser,css):
    try:
        browser.find_element_by_css_selector(css)
        return True
    except:
        return False

# 封装一个函数，用来判断属性值是否存在
def isElementPresent(driver, path):
    # 用来判断元素标签是否存在
    try:
        driver.find_element_by_xpath(path)
    # 原文是except NoSuchElementException, e:
    except NoSuchElementException as e:
        # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
        return False
    else:
        # 没有发生异常，表示在页面中找到了该元素，返回True
        return True

# 新建excel
def creatwb(wbname):
    wb=openpyxl.Workbook()
    wb.save(filename=wbname)
    print("新建Excel："+wbname+"成功")

# 保存页面数据
def write_excel(sheet_name,file_name,d_list):
    wb = Workbook()
    # 写入表头
    table_head = ['药品名称','售价','零售价','毛利','药品生产商','药品供应商']
    # 根据搜索关键字来创建sheet名称
    sheet0_name = sheet_name
    sheet0 = wb.create_sheet(sheet0_name, index=0)
    # 设置表头信息
    for i, item in enumerate(table_head):
        sheet0.cell(row = 1,column=i+1,value=item.encode('utf-8'))
    # 写入数据
    for i, data in enumerate(d_list):
        for j, item in enumerate(data):
            sheet0.cell(row = i+2,column=j+1,value=item.encode('utf-8'))
    # 保存数据
    wb.save(file_name)
    print('excel文件写入完成')

# 杀死浏览器进程
def kill_driver():
    # 杀死这个chromedriver进程，因为每次启动都会打开，所以需要kill，这里用的chrome浏览器
    os.system('chcp 65001')
    # os.system("taskkill /f /im chromedriver.exe")

# 获取网站的商品品种
def get_varieties():
    try:
        # 获取本网站商品品种
        ul = browser.find_elements_by_class_name('hang-col1')
        for li in ul:
            _li = li.find_elements_by_xpath('./div[@class="com-info"]/a')
            for _a in _li:
                # 鼠标悬停
                above = browser.find_element_by_link_text("中西成药")
                # move_to_element移到设置的元素,avove上面定位到的设置.然后执行操作
                ActionChains(browser).move_to_element(above).perform()
                # 根据名称点击操作
                mc = _a.text
                _a.click()
                sleep(3)
                browser.find_element_by_link_text("抗高血压病药").click()
                data_varieties.append(mc)

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

# 根据关键字搜索导出exlce
def export_exlce(keyword):
    # 根据搜索名称调用查询方法，并返回总页数
    total = search(keyword)
    # 组装exlce文件名称
    _exclName = keyword + "_" + nowTime + ".xlsx"
    # for i in range(2, 5):
    for i in range(2, total + 1):
        print("第", i, "页：")
        next_page(i)
    # 判断总页数大于0 并创建exlce
    if total > 0:
        # 初始化exlce文件
        creatwb(_exclName)
    # 保存数据到exlce中
    write_excel(keyword,_exclName,data_list)

# 根据品种点击搜索导出exlce
def a_export_exlce(keyword):
    # 模拟点击A标签进行搜索
    total = click_a(keyword)
    # 组装exlce文件名称
    _exclName = keyword + "_" + nowTime + ".xlsx"
    # for i in range(2, 5):
    for i in range(2, total + 1):
        print("第", i, "页：")
        next_page(i)
    # 判断总页数大于0 并创建exlce
    if total > 0:
        # 初始化exlce文件
        creatwb(_exclName)
    # 保存数据到exlce中
    write_excel(keyword,_exclName,data_list)

# 主方法
def main():
    print("*************开始爬取有货药品数据请稍等***************")
    num = int(input("请选择爬取数据选项数字：1、取文本  2、自动批量  3、单品手动输入："))
    if num == 3:
        # 关键词
        keyword = input("请输入要搜索药品名称：")
        # 导出exlce
        export_exlce(keyword)
    elif num == 2:
        # 获取所有商品品种
        get_varieties()
        for i, item in enumerate(data_varieties):
            # 根据品种点击搜索导出exlce
            a_export_exlce(item)
    elif num == 1:
        if os.path.exists("药品品种.txt"):
            with open("药品品种.txt", "r", encoding="utf-8") as f:  # 打开文件
                for line in f.readlines():
                    data = line.strip('\n')  #去掉列表中每一个元素的换行符
                    # 导出exlce
                    export_exlce(data)
        else:
            print("读取文本文件不存在，请检查！")
    else:
        print("输入选项不正确，请重新开始输入！")
        main()

    # 关闭浏览器
    browser.close()

if __name__ == "__main__":
    # key_pass = input("请输入秘钥：")
    # 校验秘钥 默认用123 md5加密
    # if key_pass=="202cb962ac59075b964b07152d234b70":
    # 登陆
    login()
    # 主方法入口
    main()
    # else :
    #     print("秘钥校验不正确，关闭该程序，重新运行！")
    #     # 关闭浏览器
    #     browser.close()
    input("请按回车键退出！")
    # 关闭浏览器进程
    kill_driver()