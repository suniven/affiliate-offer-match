import time
from selenium import webdriver


def check_if_exist(browser, element, condition):
    try:
        if condition == 'class':
            ele = browser.find_element_by_class_name(element)
        elif condition == 'id':
            ele = browser.find_element_by_id(element)
        elif condition == 'xpath':
            ele = browser.find_element_by_xpath(element)
        return ele
    except Exception as err:
        return False


def affplus_search(query):
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
        url_prefix = 'https://www.affplus.com/search?q=' + keyword + '&page='
        browser.get(url_prefix)
        # 搜索结果数量
        count = browser.find_element_by_css_selector(
            '#__layout > div > div.main.relative > div.z-10.main-wrap.relative.max-w-screen-lg.mx-auto.rounded-lg.w-full.md\:px-3 > div.flex.flex-col.lg\:flex-row.lg\:justify-between > div.mr-0.md\:mr-2.w-full.lg\:w-7\/10 > div > div > div.relative > div > div.bg-white.flex.items-center.justify-between.px-6.py-3.font-semibold.text-xs.text-gray-400.rounded-lg > div.flex.items-center.leading-loose > span.leading-none > b').text
        if count == '0':
            browser.quit()
            return results
        total_page = int(count / 2) + 1
        for page in range(1, total_page + 1):
            print("---Getting Page {0}---".format(page))
            url = url_prefix + str(page)
            browser.get(url)
            main_handle = browser.current_window_handle
            offer_links = browser.find_elements_by_css_selector('h2.mb-1 a')
            for offer_link in offer_links:
                link = offer_link.get_attribute('href')
                print("Visiting Offer: ", link)
                js = 'window.open(\"' + link + '\");'
                browser.execute_script(js)
                time.sleep(3)
                handles = browser.window_handles
                browser.switch_to.window(handles[1])  # 切换标签页
                try:
                    browser.find_element_by_xpath(
                        '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]').click()
                except:
                    continue
                handles = browser.window_handles
                browser.switch_to.window(handles[2])
                preview_url = browser.current_url
                if preview_url:
                    preview_domain = preview_url.split('/')[2]
                    if query in preview_domain:
                        print("匹配到: ", offer_link)
                        results.append(offer_link)
                browser.close()
                browser.switch_to.window(handles[1])
                browser.close()
                browser.switch_to.window(main_handle)
    except Exception as err:
        print("Error: ", err)
    finally:
        browser.quit()
        return results
