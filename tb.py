from selenium import webdriver

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')# 无头模式启动
    chrome_options.add_argument('--headless') #headless模式启动
    chrome_options.add_argument('--disable-gpu')# 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument("--start-maximized") #最大化
    chrome_options.add_argument('blink-settings=imagesEnabled=false')#不加载图片
    chromeDriverPath = r'.\tools\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chromeDriverPath, chrome_options=chrome_options)
    driver.get('http://www.baidu.com/')
    html = driver.page_source#获取网页信息
    print(html)
    driver.close()

if __name__ == '__main__':
    main()