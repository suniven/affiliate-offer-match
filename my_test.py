from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import pandas as pd

with open('./query.txt', 'r') as f:
    list=f.readlines()
keyword=[]
for domain in list:
    a = '.'.join(domain.strip().split('.')[-2:])
    if len(a)>2:
        keyword.append(a)
df = pd.DataFrame(keyword, columns=["keyword"])
df.to_csv('./keyword.csv', index=False)