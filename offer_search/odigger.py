import re
import time
from selenium import webdriver

MAX_REFRESH_TIME = 20


def check_if_exist(browser, element, condition):
    try:
        if condition == 'class':
            browser.find_element_by_class_name(element)
        elif condition == 'id':
            browser.find_element_by_id(element)
        elif condition == 'xpath':
            browser.find_element_by_xpath(element)
        elif condition == 'css':
            browser.find_element_by_css_selector(element)
        return True
    except Exception as err:
        return False


def odigger_search(query):
    # # 正常模式
    # browser = webdriver.Chrome()
    # browser.maximize_window()
    # headless模式
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=option)
    results = []
    try:
        keyword = query.split('.')[-2]
        print("Keyword: ", keyword)
        page = 1
        while True:
            url = 'https://odigger.com/offers?search=' + keyword + '&page=' + str(page)
            print("---Current Page: {0}---".format(page))
            browser.get(url)
            time.sleep(4)
            trs = browser.find_elements_by_css_selector('#search-page-offers-table > tbody > tr')
            if not trs:
                print("没结果")
                return results
            main_handle = browser.current_window_handle
            for tr in trs:
                offer_link = tr.find_element_by_css_selector('h6 > a').get_attribute('href')
                print("--- Getting Offer {0} ---".format(offer_link))
                js = 'window.open(\"' + offer_link + '\");'
                browser.execute_script(js)
                time.sleep(2)
                handles = browser.window_handles
                browser.switch_to.window(handles[1])  # 切换标签页

                tbody = browser.find_element_by_xpath(
                    '//*[@id="app"]/section/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div/table/tbody')
                trs = tbody.find_elements_by_tag_name('tr')
                for tr in trs:
                    td_1 = tr.find_elements_by_tag_name('td')[0]
                    td_2 = tr.find_elements_by_tag_name('td')[1]
                    if td_1.text == 'Preview:':
                        if td_2.find_element_by_tag_name('a').get_attribute('href'):
                            preview_url = td_2.find_element_by_tag_name('a').get_attribute('href')
                            if preview_url:
                                preview_domain = preview_url.split('/')[2]
                                if query in preview_domain:
                                    print("匹配到: ", offer_link)
                                    results.append(offer_link)
                browser.close()
                browser.switch_to.window(main_handle)

            # 看看是不是到最后一页了
            page += 1
            browser.get('https://odigger.com/offers?search=' + keyword + '&page=' + str(page))
            cur_page = re.findall(r'page=[0-9]+', browser.current_url)[0][5:]
            if cur_page == '1':
                break
    except Exception as err:
        print(err)
    finally:
        browser.quit()
        return results
