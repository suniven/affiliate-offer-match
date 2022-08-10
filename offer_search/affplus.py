import re
import sys
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import and_, asc, desc, or_
from offer_search.model import Affpay_Offer
from bs4 import BeautifulSoup

# 共77种category
category_list = [
    "Mobile", "CPL", "SOI", "Sweepstake", "Incent", "Android", "Dating", "Nutra", "Crypto", "Ecommerce", "iOS", "CPS",
    "BizOpp", "Shopping", "Forex", "Health", "Game", "CPI", "Adult", "Finance", "Entertainment", "Pin", "Gambling",
    "App", "Email", "DOI", "Download", "Casino", "Survey", "Job", "Subscription", "COD", "Desktop", "CPE", "Diet",
    "RevShare", "Freebie", "Software", "Beauty", "Insurance", "Coupon", "Leadgen", "Utility", "Trial", "Mainstream",
    "PPS", "Home", "CPR", "Service", "Auto", "VOD", "Fitness", "PPL", "Betting", "Sport", "Travel", "LifeStyle",
    "Business", "Install", "Smartlink", "Loan", "Credit", "Education", "Cam", "Solar", "CPC", "CBD", "Streaming",
    "Binary", "Payday", "Real Estate", "Pay Per Call", "Astrology", "Music", "Legal", "KPI", "Auctions"
]

# url_prefix = 'https://www.affplus.com/search?verticals=Adult&sort=time_desc&page='  # 后面加页数
# url_prefix = 'https://www.affplus.com/search?verticals=Dating&sort=time_desc&page='  # 后面加页数

START_PAGE = 1
END_PAGE = 200
PAGE_COUNT = 200
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
proxy = '127.0.0.1:1080'
proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}


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


def get_offer(offer_link, browser, session):
    print("--------------------------------")
    print("Visiting Offer: ", offer_link)
    js = 'window.open(\"' + offer_link + '\");'
    browser.execute_script(js)
    time.sleep(3)
    handles = browser.window_handles
    browser.switch_to.window(handles[1])  # 切换标签页
    affpay_offer = Affpay_Offer()
    affpay_offer.url = offer_link
    affpay_offer.title = ''
    affpay_offer.status = ''
    affpay_offer.offer_create_time = ''
    affpay_offer.offer_update_time = ''
    try:
        affpay_offer.title = browser.find_element_by_css_selector('h1.richtext').text
        # print("title: ", affpay_offer.title)
        container = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div')
        spans = container.find_elements_by_tag_name('span')
        affpay_offer.status = spans[0].text
        # print("status: ", affpay_offer.status)
        affpay_offer.offer_create_time = spans[1].text
        # print("create: ", affpay_offer.offer_create_time)
        affpay_offer.offer_update_time = spans[2].text
        # print("update: ", affpay_offer.offer_update_time)
    except Exception as err:
        print("Error: ", err)

    try:
        affpay_offer.network = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/h3'
        ).text
        # print("network: ", affpay_offer.network)

        affpay_offer.payout = ''
        affpay_offer.category = ''
        affpay_offer.geo = ''
        divs = browser.find_elements_by_xpath(
            '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div')
        for div in divs:
            spans = div.find_elements_by_tag_name('span')
            if spans[0].text == 'PAYOUT':
                affpay_offer.payout = spans[1].text + '/' + spans[2].text
                # print("payout: ", affpay_offer.payout)
            elif spans[0].text == 'CATEGORY':
                affpay_offer.category = spans[1].text
                # print("category: ", affpay_offer.category)
            elif spans[0].text == 'GEO':
                # geos = []
                # for span in spans:
                #     if span.text == 'GEO':
                #         continue
                #     else:
                #         geos.append(span.text)  # 折叠的span.text为空 就离谱
                # print("geos: ", geos[:])
                # affpay_offer.geo = ' '.join(geos)

                # 测试 用soup可以
                soup = BeautifulSoup(div.get_attribute('innerHTML'), "lxml")
                geos = soup.get_text()[4:].replace("GEOs", "")
                geos = " ".join(re.sub(r"[0-9]+", "", geos).split("\n"))
                geos = " ".join(geos.split())
                affpay_offer.geo = geos
                # print("geo: ", affpay_offer.geo)

    except Exception as err:
        print("Error: ", err)

    affpay_offer.land_page_img = ''
    affpay_offer.land_page = ''
    try:
        browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]').click()

        handles = browser.window_handles
        browser.switch_to.window(handles[2])
        if 'The Geek Gaming Smartlink' in affpay_offer.title:  # 先这样吧懒得管了
            affpay_offer.land_page = 'about:blank'
        else:
            affpay_offer.land_page = browser.current_url

        browser.close()
        browser.switch_to.window(handles[1])
    except Exception as err:
        print("Getting Preview Landing Page Error: ", err)

    # description 麻烦死了
    affpay_offer.description = ''
    try:
        show_more_btn = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[3]/div/div/span')
        show_more_btn.click()
    except Exception as err:
        print("No Show More Btn.")
        # print("Error Detail: ", err)
    try:
        # 情况太多，直接处理html算了
        description = browser.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[3]/div').get_attribute(
                'innerHTML')
        soup = BeautifulSoup(description, "lxml")
        description = soup.get_text()
        affpay_offer.description = description
    except Exception as err:
        print("Getting Description Error: ", err)
    affpay_offer.create_time = get_now_timestamp()

    # for test
    print("offer title: ", affpay_offer.title)
    print("offer status: ", affpay_offer.status)
    print("offer create time: ", affpay_offer.offer_create_time)
    print("offer update time: ", affpay_offer.offer_update_time)
    print("offer description: ", affpay_offer.description)
    print("offer land page: ", affpay_offer.land_page)
    print("offer land page img: ", affpay_offer.land_page_img)
    print("offer category: ", affpay_offer.category)
    print("offer geo: ", affpay_offer.geo)
    print("offer network: ", affpay_offer.network)
    print("offer payout: ", affpay_offer.payout)
    print("time: ", affpay_offer.create_time)

    session.add(affpay_offer)
    session.commit()


if __name__ == '__main__':
    # # 正常模式
    # browser = webdriver.Chrome()
    # browser.maximize_window()
    # headless模式
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=option)
    browser.implicitly_wait(10)
    engine = create_engine(sqlconn, echo=True, max_overflow=8)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    category = category_list[int(sys.argv[1])]
    url_prefix = 'https://www.affplus.com/search?verticals=' + category + '&page='

    for i in range(START_PAGE, END_PAGE + 1):
        print("--------------------")
        print("Getting Page {0}...".format(i))
        url = url_prefix + str(i)
        browser.get(url)
        main_handle = browser.current_window_handle
        offer_links = browser.find_elements_by_css_selector('h2.mb-1 a')
        for offer_link in offer_links:
            link = offer_link.get_attribute('href')
            # 检查是否已经爬取过这个offer了
            rows = session.query(Affpay_Offer).filter(Affpay_Offer.url.like(link)).all()
            if rows:
                print("Offer {0} Has Already Been Visited.".format(link))
                continue
            # 弹窗处理测试
            # link = 'https://www.affplus.com/o/iluvo-de-de-ch-at-non-incent-cpl-mobile-2'
            # 折叠geo获取测试
            # link = 'https://www.affplus.com/o/sweetsext-au-ca-dk-ie-nz-no-gb-us-cpl-for-adult-dating-content-18-women-date-sex-sexy-tinder-flirt'
            get_offer(link, browser, session)
            browser.close()
            browser.switch_to.window(main_handle)
            # break  # for test
        # break  # for test
    browser.quit()
    session.close()
