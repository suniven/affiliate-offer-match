# 大修 搜索结果先看是否匹配 返回offer页面的链接


import re
import time
from selenium import webdriver


def check_if_exist(browser, element, condition):
    try:
        if condition == 'class':
            browser.find_element_by_class_name(element)
        elif condition == 'id':
            browser.find_element_by_id(element)
        elif condition == 'xpath':
            browser.find_element_by_xpath(element)
        return True
    except Exception as err:
        return False


def get_next_page(browser, retry, next_page_xpath):
    try:  # 可能出错 stale element reference: element is not attached to the page document
        if retry == 10:
            return
        next_page = browser.find_element_by_xpath(next_page_xpath)
        next_page.click()
        time.sleep(3)
        retry = 0
        return
    except:
        retry = retry + 1
        print("Try Again.")
        get_next_page(browser, retry, next_page_xpath)


def offervault_search(query):
    # # 正常模式
    # browser = webdriver.Chrome()
    # browser.maximize_window()
    # headless模式
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=option)
    browser.implicitly_wait(10)
    results = []
    try:
        keyword = query.split('.')[-2]
        print("Keyword: ", keyword)
        url = 'https://offervault.com/?selectedTab=topOffers&search=' + keyword + '&page=1'
        browser.get(url)
        while True:
            main_handle = browser.current_window_handle
            url = browser.current_url
            page = re.findall(r'page=[0-9]+', url)[0][5:]
            print("-------Current Page: {0}-------".format(page))
            # 获取当前页offer链接
            container = browser.find_element_by_css_selector('#index-page-offerstable > tbody')
            links = container.find_elements_by_tag_name('a')
            if not links:
                print("未找到符合条件的搜索结果。")
                return results
            for link in links:
                offer_link = link.get_attribute('href')
                # 过滤 javascript:;
                if offer_link == 'javascript:;':
                    continue
                print("---Visiting Offer: {0}...".format(offer_link))
                js = 'window.open(\"' + offer_link + '\");'
                browser.execute_script(js)
                time.sleep(2)
                handles = browser.window_handles
                browser.switch_to.window(handles[1])  # 切换标签页
                # 获得preview landing page
                try:
                    tbody = browser.find_element_by_xpath(
                        '//*[@id="__layout"]/div/section/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/table/tbody'
                    )
                    # 防止像affpay一样有的项没有
                    items = tbody.find_elements_by_tag_name('tr')
                    for item in items:
                        th = item.find_element_by_tag_name('th').text
                        td = item.find_element_by_tag_name('td')
                        if th == 'Preview:':
                            preview_url = td.find_element_by_tag_name('a').get_attribute('href')
                            if preview_url:
                                preview_domain = preview_url.split('/')[2]
                                if query in preview_domain:
                                    print("匹配到: ", offer_link)
                                    results.append(offer_link)
                except Exception as err:
                    print("Error: ", err)
                browser.close()
                browser.switch_to.window(main_handle)
                time.sleep(1)
            # 判断是否还有下一页
            btn_count = len(
                browser.find_elements_by_css_selector(
                    '#__layout > div > section:nth-child(3) > div > div > div > div.col-md-9 > div.tablecont > div > div > div.paginrow > ul > li'
                ))
            next_page_index = btn_count - 1
            next_page_xpath = '//*[@id="__layout"]/div/section[2]/div/div/div/div[1]/div[1]/div/div/div[2]/ul/li[' + str(
                next_page_index) + ']/button'
            if not check_if_exist(browser, next_page_xpath, 'xpath'):
                break
            else:
                # 跳转到下一页
                get_next_page(browser, 0, next_page_xpath)
    except Exception as err:
        print(err)
    finally:
        browser.quit()
        return results


if __name__ == '__main__':
    offervault_search('teenfinder')
