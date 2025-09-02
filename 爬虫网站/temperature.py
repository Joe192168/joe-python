import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 区县中文名称映射
district_names = {
    "yongchuan": "永川",
    "hechuan": "合川",
    "nanchuan": "南川",
    "jiangjin": "江津",
    "changshou": "长寿",
    "qianjiang": "黔江",
    "wanzhou": "万州",
    "fuling": "涪陵",
    "chengkou": "城口",
    "yunyang": "云阳",
    "wuxi": "巫溪",
    "fengjie": "奉节",
    "tongnan": "潼南",
    "dianjiang": "垫江",
    "liangping": "梁平",
    "dazu": "大足",
    "rongchang": "荣昌",
    "tongliang": "铜梁",
    "bishan": "璧山",
    "fengdu": "丰都",
    "wulong": "武隆",
    "qijiang": "綦江",
    "zhongxian": "忠县",
    "wushan": "巫山",
    "shizhu": "石柱",
    "xiushan": "秀山",
    "youyang": "酉阳",
    "pengshui": "彭水",
    "kaizhou": "开州",
    "wansheng": "万盛",
    "kaixian": "开县"
}

def get_monthly_avg_temperature(district, year="2025"):
    """获取指定区县指定年份的月度平均气温数据"""
    url = f"https://www.tianqi24.com/{district}/history.html"
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "year"))
        )
        
        print(f"正在访问: {url}")
        
        # 检查年份选项是否存在
        year_select = Select(driver.find_element(By.ID, "year"))
        available_years = [option.get_attribute('value') for option in year_select.options if option.get_attribute('value')]
        print(f"可用年份: {available_years}")
        
        # 如果指定年份不存在，尝试使用2024年
        if year not in available_years:
            print(f"{year}年数据不可用，尝试使用2025年")
            year = "2025" if "2025" in available_years else (available_years[0] if available_years else "2025")
        
        # 确保year是字符串类型
        year = str(year)
        
        # 选择年份
        year_select.select_by_value(year)
        print(f"已选择年份: {year}")
        
        # 点击查询按钮
        query_button = driver.find_element(By.CLASS_NAME, "btn")
        query_button.click()
        print(f"已点击查询按钮")
        
        # 等待页面更新
        time.sleep(2)  # 增加等待时间
        
        # 获取更新后的页面HTML
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找包含月度数据的列表结构
        monthly_data = []
        
        # 查找包含月度气温数据的ul列表
        article_sections = soup.find_all('article')
        print(f"找到 {len(article_sections)} 个 article 元素")
        
        for i, article in enumerate(article_sections):
            if not isinstance(article, Tag):
                continue
                
            # 查找包含"每月平均气温数据"或年份信息的文章
            header = article.find('header')
            if header:
                header_text = header.get_text()
                print(f"Article {i} header: {header_text[:50]}...")
                
                # 扩大匹配条件，包括多种可能的标题格式
                if ('每月平均气温数据' in header_text or 
                    f'{year}年每月平均气温数据' in header_text or
                    f'气温数据' in header_text):
                    print(f"找到目标文章: {header_text}")
                    
                    # 在这个文章中查找ul列表
                    ul_list = article.find('ul', class_='col7')
                    if ul_list and isinstance(ul_list, Tag):
                        print(f"找到数据列表")
                        
                        # 获取所有数据行（跳过表头）
                        li_items = ul_list.find_all('li')[1:]  # 跳过第一个li（表头）
                        print(f"找到 {len(li_items)} 行数据")
                        
                        for j, li in enumerate(li_items):
                            if not isinstance(li, Tag):
                                continue
                            
                            divs = li.find_all('div')
                            if len(divs) >= 7:  # 确保有足够的列数据
                                # 第一个div是月份，第二个是高温，第三个是低温，第七个是总降雨
                                month_text = divs[0].get_text(strip=True)
                                high_temp_text = divs[1].get_text(strip=True)
                                low_temp_text = divs[2].get_text(strip=True)
                                rainfall_text = divs[6].get_text(strip=True)  # 总降雨量
                                
                                print(f"行 {j}: {month_text} | {high_temp_text} | {low_temp_text} | 降雨量: {rainfall_text}")
                                
                                # 提取高温数据
                                high_temp_match = re.search(r'(-?\d+)℃', high_temp_text)
                                # 提取低温数据
                                low_temp_match = re.search(r'(-?\d+)℃', low_temp_text)
                                # 提取降雨量数据
                                rainfall_match = re.search(r'(\d+\.?\d*)', rainfall_text)
                                
                                if high_temp_match and low_temp_match:
                                    high_temp = float(high_temp_match.group(1))
                                    low_temp = float(low_temp_match.group(1))
                                    avg_temp = (high_temp + low_temp) / 2  # 计算平均温度
                                    rainfall = float(rainfall_match.group(1)) if rainfall_match else 0.0
                                    
                                    monthly_data.append({
                                        '区县中文名称': district_names.get(district, district),
                                        '区县': district,
                                        '年份': year,
                                        '月份': month_text,
                                        '高温': high_temp,
                                        '低温': low_temp,
                                        '平均气温': round(avg_temp, 1),
                                        '总降水量': rainfall
                                    })
                                    print(f"成功解析: {month_text} 高温{high_temp}℃ 低温{low_temp}℃ 降水量{rainfall}mm")
                                else:
                                    print(f"无法解析温度数据: {high_temp_text}, {low_temp_text}")
                    else:
                        print(f"未找到col7类型的ul列表")
                    break  # 找到数据后跳出循环
        
        print(f"最终获取到 {len(monthly_data)} 条数据")
        return monthly_data
        
    except Exception as e:
        print(f"获取{district} {year}年数据时出错: {str(e)}")
        # 打印更详细的错误信息
        import traceback
        traceback.print_exc()
        return []
    finally:
        if driver:
            driver.quit()

def crawl_all_districts_data(year="2025"):
    """爬取所有区县指定年份的数据"""
    all_data = []
    
    for district in district_names.keys():
        print(f"正在爬取{district} {year}年的数据...")
        data = get_monthly_avg_temperature(district, year)
        if data:
            all_data.extend(data)
        # 添加延迟避免请求过于频繁
        time.sleep(2)  # 增加延迟时间，因为Selenium需要更多时间
    
    return all_data

def save_to_csv(data, filename):
    """保存数据到CSV文件"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"数据已保存到 {filename}")

def test_single_district(district_name="yongchuan", year="2025"):
    """测试单个区县指定年份的数据抓取"""
    print(f"测试爬取{district_name} {year}年的数据...")
    data = get_monthly_avg_temperature(district_name, year)
    
    if data:
        print(f"成功获取 {len(data)} 条数据:")
        for item in data[:3]:  # 显示前3条
            print(f"  {item['区县中文名称']}({item['区县']}) {item['年份']}年 - {item['月份']}: 高温{item['高温']}℃, 低温{item['低温']}℃, 平均{item['平均气温']}℃, 降水{item['总降水量']}mm")
        return True
    else:
        print("未能获取任何数据")
        return False

# 主程序
if __name__ == "__main__":
    target_year = "2025"  # 改为2024年，因为2025年数据可能还不完整
    print(f"开始爬取重庆各区县{target_year}年月度平均气温数据...")
    
    # 先测试一个区县
    if test_single_district("yongchuan", target_year):
        print(f"\n单个区县{target_year}年测试成功，开始爬取所有区县...")
        
        # 爬取所有区县数据
        all_data = crawl_all_districts_data(target_year)
        
        if all_data:
            # 保存数据到CSV文件
            filename = f"chongqing_{target_year}_monthly_avg_temperature.csv"
            save_to_csv(all_data, filename)
            
            # 打印数据统计
            print(f"\n成功爬取 {len(all_data)} 条{target_year}年月度气温数据")
            print(f"涵盖 {len(set([d['区县'] for d in all_data]))} 个区县")
            
            # 显示前几条数据作为示例
            print("\n数据示例:")
            for i, item in enumerate(all_data[:5]):
                print(f"{item['区县中文名称']}({item['区县']}) {item['年份']}年 - {item['月份']}: 高温{item['高温']}℃, 低温{item['低温']}℃, 平均{item['平均气温']}℃, 降水{item['总降水量']}mm")
        else:
            print("未能获取任何数据")
    else:
        print(f"单个区县{target_year}年测试失败，请检查网络连接或网站结构是否发生变化")