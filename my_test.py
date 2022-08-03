from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument("--window-size=1920,1080")
browser = webdriver.Chrome(chrome_options=option)
browser.implicitly_wait(10)
url = 'https://offervault.com/?selectedTab=topOffers&search=' + 'wellhellooo' + '&page=1'
browser.get(url)
container = browser.find_element_by_css_selector('#index-page-offerstable > tbody')
links = container.find_elements_by_tag_name('a')
print(links[:])