import os
import re
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from offer_search.model import Offervault_Offer


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


def get_offer(browser, offer_link):
    print("---Visiting Offer: {0}...".format(offer_link))
    js = 'window.open(\"' + offer_link + '\");'
    browser.execute_script(js)
    time.sleep(2)
    handles = browser.window_handles
    browser.switch_to.window(handles[1])  # 切换标签页

    offervault_offer = Offervault_Offer()
    offervault_offer.url = offer_link
    offervault_offer.title = ''
    offervault_offer.payout = ''
    offervault_offer.category = ''
    offervault_offer.network = ''
    offervault_offer.offer_update_time = ''
    offervault_offer.geo = ''
    offervault_offer.description = ''
    offervault_offer.land_page_img = ''
    offervault_offer.land_page = ''
    # 本来就没有
    offervault_offer.offer_create_time = ''
    try:
        tbody = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/section/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/table/tbody')
        # 防止像affpay一样有的项没有
        items = tbody.find_elements_by_tag_name('tr')
        for item in items:
            th = item.find_element_by_tag_name('th').text
            td = item.find_element_by_tag_name('td')
            if th == 'Offer Name:':
                offervault_offer.title = td.text
            elif th == 'Payout:':
                offervault_offer.payout = td.text
            elif th == 'Categories:':
                offervault_offer.category = td.text
            elif th == 'Network:':
                offervault_offer.network = td.text
            elif th == 'Last Updated:':
                offervault_offer.offer_update_time = td.text
            elif th == 'Countries:':
                # 麻烦死了
                try:
                    # 要展开的
                    a = td.find_element_by_tag_name('a').click()
                    # ul = browser.find_element_by_xpath('//*[@id="__bv_popover_116__"]/div[2]/div/ul')
                    # 太狗了 id 是动态变化的 要自己写xpath
                    ul = browser.find_element_by_css_selector(
                        'div.popover > div.popover-body > div.country-popovr > ul')
                    countries = ul.find_elements_by_tag_name('a')
                    geos = []
                    for country in countries:
                        # print("country: ", country.text)
                        geos.append(country.text)
                    offervault_offer.geo = ' '.join(geos)
                except Exception as err:
                    # 不用展开的
                    spans = td.find_elements_by_tag_name('span')
                    geos = []
                    for span in spans:
                        if span.text:
                            # print("span: ", span.text)
                            geos.append(span.text)
                    geos = list(set(geos))  # 不知道为什么会有重复的不想找原因了反正就这样去个重算了
                    offervault_offer.geo = ' '.join(geos)
            elif th == 'Preview:':
                try:
                    offervault_offer.land_page = td.find_element_by_tag_name('a').get_attribute('href')
                except Exception as err:
                    print("No Preview Available.")
                    print(err)

    except Exception as err:
        print(err)

    try:
        offervault_offer.description = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/section/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div').text
    except Exception as err:
        print("No Description.")
        print(err)
    return offervault_offer
    # for test
    print("offer title: ", offervault_offer.title)
    print("offer payout: ", offervault_offer.payout)
    print("offer geo: ", offervault_offer.geo)
    print("offer network: ", offervault_offer.network)
    print("offer update time: ", offervault_offer.offer_update_time)
    print("offer category: ", offervault_offer.category)
    print("offer landing page: ", offervault_offer.land_page)


def get_next_page(browser, retry):
    try:  # 可能出错 stale element reference: element is not attached to the page document
        if retry == 10:
            return
        next_page = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/section[2]/div/div/div/div[1]/div[1]/div/div/div[2]/ul/li[10]/button')
        next_page.click()
        time.sleep(2)
        retry = 0
        return
    except:
        retry = retry + 1
        print("Try Again.")
        get_next_page(browser, retry)


def offervault_search(keyword):
    # # 正常模式
    # browser = webdriver.Chrome()
    # browser.maximize_window()
    # headless模式
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=option)
    browser.implicitly_wait(10)

    try:
        df = pd.DataFrame(columns=[
            'keyword', 'url', 'title', 'payout', 'offer_create_time', 'offer_update_time', 'category', 'geo', 'network',
            'description', 'landing_page'
        ])
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
                return None
            for link in links:
                offer_link = link.get_attribute('href')
                # 过滤 javascript:;
                if offer_link == 'javascript:;':
                    continue
                offer_info = get_offer(browser, offer_link)
                df.loc[len(df)] = [
                    keyword, offer_info.url, offer_info.title, offer_info.payout, offer_info.offer_create_time,
                    offer_info.offer_update_time, offer_info.category, offer_info.geo, offer_info.network,
                    offer_info.description, offer_info.land_page
                ]
                browser.close()
                browser.switch_to.window(main_handle)

            # 判断是否还有下一页
            if not check_if_exist(
                    browser,
                    '//*[@id="__layout"]/div/section[2]/div/div/div/div[1]/div[1]/div/div/div[2]/ul/li[10]/button',
                    'xpath'):
                break
            else:
                # 跳转到下一页
                get_next_page(browser, 0)
    except Exception as err:
        print(err)
    finally:
        browser.quit()
        return df


if __name__ == '__main__':
    offervault_search('wellhello')
