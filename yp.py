import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
import json
import csv
from lxml import etree

#options = webdriver.ChromeOptions()
#options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
#不加载图片
browser = webdriver.Chrome()
browser.maximize_window()# 窗口最大化 <br>>>> #模拟鼠标悬浮
wait =WebDriverWait(browser,50)#设置等待时间
url = 'http://www.shanyaoo.com/'
data_list= []#设置全局变量用来存储数据
keyword ="药"#关键词

def search():
    browser.get(url)

    browser.find_element_by_xpath('//input[@placeholder="用户名"]').send_keys('xs25391')
    browser.find_element_by_xpath('//input[@placeholder="登录密码"]').send_keys('123456')
    browser.find_element_by_xpath('//button[@class="loginBtn"]').click()
    try:
        input = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.search-input"))
        )  #等到搜索框加载出来
        submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='searchForm ']/div/button[1]"))
        )#等到搜索按钮可以被点击
        input[0].send_keys(keyword)#向搜索框内输入关键词
        submit.click()#点击
        # total = wait.until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/table/tbody/tr/td[2]/div[3]/div[2]/div[42]/div/span/text()[1]')
        #     )
        # )
        #记录一下总页码,等到总页码加载出来
        # # 滑动到底部，加载出后三十个货物信息
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait.until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#J_goodsList > ul > li:nth-child(60)"))
        # )
        html = browser.page_source#获取网页信息
        time.sleep(20)#设置随机延迟
        prase_html(html)#调用提取数据的函数
        #返回总页数
        return 10
    except TimeoutError:
        search()

def next_page(page_number):
    try:
        # 滑动到底部
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 3))#设置随机延迟
        button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'nextpage'))
        )#翻页按钮
        button.click()# 翻页动作
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='nohide_one']"))
        )#等到30个商品都加载出来
        # 滑动到底部，加载出后三十个货物信息
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='nohide_one']"))
        )#等到60个商品都加载出来
        wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "cur"), str(page_number))
        )# 判断翻页成功,高亮的按钮数字与设置的页码一样
        html = browser.page_source#获取网页信息
        time.sleep(25)#设置随机延迟
        #browser.find_element_by_link_text("只看有货").click()#模拟用户点击
        #调用提取数据的函数
        prase_html(html)
    except TimeoutError:
        return next_page(page_number)


def prase_html(html):
    html = etree.HTML(html)
    # 开始提取信息,找到ul标签下的全部li标签
    try:
        lis = browser.find_elements_by_class_name('pl-skin')
        # 遍历
        for pl in lis:
            #判断有禁售药品或下架
            if pl.get_attribute("id")=="nohide_one":
                # 药品名称
                title = pl.find_element_by_xpath('.//div[@class="p-caption"]//a').text
                # 售价
                price = pl.find_element_by_xpath('.//span[@class="price"]//em')
                # 销量
                sale = pl.find_element_by_xpath('.//span[@class="p-sale"]//em')
                # 阶梯满减或满减
                li_caption = pl.find_elements_by_xpath('.//li[@class="promt_li"]//a')
                if price.text:
                    price = price.text
                else:
                    price = "商家尚未定价"
                if sale:
                    sale = sale.text
                else:
                    sale = None
                if li_caption:
                    # for labx in li_caption:
                    if li_caption[0].text=="阶梯满减":
                        j_promt_caption = li_caption[1].get_attribute("innerHTML")
                        m_promt_caption = li_caption[3].get_attribute("innerHTML")
                    elif li_caption[0].text=="满减":
                        j_promt_caption = li_caption[1].get_attribute("innerHTML")
                        m_promt_caption = None
                    elif li_caption[2].text=="满减":
                        j_promt_caption = None
                        m_promt_caption = li_caption[3].get_attribute("innerHTML")
                    else:
                        j_promt_caption = None
                        m_promt_caption = None
                else:
                    j_promt_caption = None
                    m_promt_caption = None
                data_dict ={}#写入字典
                data_dict["药名称"] = title
                data_dict["售价"] = price
                data_dict["销量"] = sale
                data_dict["阶梯满减"] = j_promt_caption
                data_dict["满减"] = m_promt_caption
                print(data_dict)
                data_list.append(data_dict)#写入全局变量
    except TimeoutError:
        prase_html(html)

def save_html():
    content = json.dumps(data_list, ensure_ascii=False, indent=2)
    #把全局变量转化为json数据
    with open("yp.json", "a+", encoding="utf-8") as f:
        f.write(content)
        print("json文件写入成功")

    with open('yp.csv', 'w', encoding='utf-8', newline='') as f:
        # 表头
        title = data_list[0].keys()
        # 声明writer
        writer = csv.DictWriter(f, title)
        # 写入表头
        writer.writeheader()
        # 批量写入数据
        writer.writerows(data_list)
    print('csv文件写入完成')

def main():
    print("第", 1, "页：")
    total = int(search())
    for i in range(2, 5):
        # for i in range(2, total + 1):
        time.sleep(25)  # 设置随机延迟
        print("第", i, "页：")
        next_page(i)
    save_html()


if __name__ == "__main__":
    main()