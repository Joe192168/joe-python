from playwright.sync_api import sync_playwright
import time
import json
import random

# 设置要爬取的游戏名称
TARGET_GAMES = ["天涯明月刀","王者荣耀"]  # 替换为您要爬取的游戏名称

def extract_filter_data(page):
    """从页面提取筛选数据，形成{label: [options]}结构"""
    # 点击所有展开按钮
    def expand_all():
        # 点击展开按钮
        expand_buttons = page.locator("div.down:visible").all()
        for button in expand_buttons:
            try:
                if button.is_visible():
                    button.scroll_into_view_if_needed()
                    button.click()
                    print("  点击展开按钮")
                    time.sleep(0.3)
            except:
                pass
        
        # 点击更多按钮
        more_buttons = page.locator("div.opt-more:visible").all()
        for button in more_buttons:
            try:
                if button.is_visible():
                    button.scroll_into_view_if_needed()
                    button.click()
                    print("  点击更多按钮")
                    time.sleep(0.3)
            except:
                pass
    
    # 确保所有内容展开
    expand_all()
    time.sleep(1)  # 确保内容加载
    
    # 提取筛选数据
    filter_data = {}
    
    # 获取所有筛选类别
    filter_items = page.locator('div.filter-item')
    filter_count = filter_items.count()
    
    for i in range(filter_count):
        item = filter_items.nth(i)
        
        try:
            # 提取类别名称
            label_element = item.locator('div.filter-item-label')
            if label_element.count() > 0:
                label = label_element.text_content().strip()
                
                # 提取该类别下的所有选项
                options = []
                option_elements = item.locator('div.opt-item')
                option_count = option_elements.count()
                
                for j in range(option_count):
                    option = option_elements.nth(j).text_content().strip()
                    options.append(option)
                
                # 添加到结果字典
                filter_data[label] = options
        except Exception as e:
            print(f"提取筛选类别时出错: {str(e)}")
    
    return filter_data

def crawl_target_games():
    results = []
    
    with sync_playwright() as p:
        try:
            # 启动浏览器
            browser = p.chromium.launch(
                headless=False,
                slow_mo=100,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                viewport={"width": 1200, "height": 800}
            )
            page = context.new_page()
            page.set_default_timeout(60000)
            
            print(f"开始爬取目标游戏: {', '.join(TARGET_GAMES)}")
            print("访问网站: https://www.pzds.com/gameList")
            
            # 访问游戏列表页
            page.goto("https://www.pzds.com/gameList", wait_until="domcontentloaded")
            time.sleep(random.uniform(2, 4))
            
            # 等待游戏列表加载
            page.wait_for_selector("div.list_content", timeout=15000)
            
            for game_name in TARGET_GAMES:
                print(f"\n搜索游戏: {game_name}")
                game_found = False
                game_items = page.locator("div.list_content a.content_item").all()
                
                for idx, item in enumerate(game_items):
                    try:
                        title_element = item.locator("div.text-565").first
                        if title_element.is_visible():
                            title = title_element.text_content().strip()
                            
                            if game_name == title:
                                print(f"找到匹配游戏: {title}")
                                
                                # 点击进入游戏详情页
                                print(f"点击进入游戏详情页")
                                with page.expect_navigation():
                                    item.click()
                                time.sleep(random.uniform(2, 3))
                                
                                # 等待详情页加载
                                try:
                                    page.wait_for_selector("div.filter-content", timeout=15000)
                                    print("详情页加载完成")
                                except:
                                    print("详情页加载超时，继续尝试提取")
                                
                                # 提取筛选数据
                                filter_data = extract_filter_data(page)
                                results.append({
                                    "game_name": game_name,
                                    "filters": filter_data
                                })
                                
                                # 计算统计信息
                                filter_count = len(filter_data)
                                option_count = sum(len(options) for options in filter_data.values())
                                print(f"提取成功: {filter_count} 个筛选类别，共 {option_count} 个选项")
                                
                                # 返回列表页
                                page.go_back()
                                print("返回到游戏列表页")
                                time.sleep(random.uniform(2, 3))
                                page.wait_for_selector("div.list_content", timeout=15000)
                                
                                game_found = True
                                break
                    except Exception as e:
                        print(f"处理游戏元素时出错: {str(e)}")
                
                if not game_found:
                    print(f"未找到匹配 '{game_name}' 的游戏")
                    results.append({
                        "game_name": game_name,
                        "status": "not found"
                    })
            
            # 关闭浏览器
            context.close()
            browser.close()
        
        except Exception as e:
            print(f"爬取过程中发生错误: {str(e)}")
            # 保存错误信息
            page.screenshot(path="error_screenshot.png")
            html = page.content()
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(html)
    
    # 保存结果到JSON文件
    if results:
        with open("game_filter_data.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 打印爬取结果
        print("\n爬取结果:")
        for game in results:
            if "status" in game:
                print(f" × 未找到: {game['game_name']}")
            else:
                print(f" ✓ {game['game_name']}:")
                for label, options in game['filters'].items():
                    print(f"   - {label}: {len(options)} 个选项")
        
        print(f"\n结果已保存到 game_filter_data.json")
    else:
        print("未能获取任何游戏数据")

if __name__ == "__main__":
    crawl_target_games()