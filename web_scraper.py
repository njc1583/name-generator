#!/usr/bin/python

import sys
import os
import re
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import pandas as pd 

driver = webdriver.Chrome(executable_path="C:/Executables/chromedriver.exe")

# driver = webdriver.Chrome()

driver.get("https://en.wikipedia.org/wiki/List_of_towns_in_England")

content = driver.page_source
soup = BeautifulSoup(content)

tables = soup.findAll('table', attrs={'class': 'wikitable sortable jquery-tablesorter'})

cities = {}
cities['England'] = []

title_regex = re.compile('.+')

for table in tables:
    for td_href in table.find_all('a', href=True, attrs={'title': title_regex}):
        cities['England'].append(td_href.text)

# print(cities)

with open('city_data.json', 'w') as outfile:
    json.dump(cities, outfile, indent=4)

# options = ChromeOptions()
# options.binary_location = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"

# print("getcwd()", os.getcwd())

# driver_path = os.path.join(os.getcwd(), "chromedriver")
# driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)

# driver.get("https://en.wikipedia.org/wiki/List_of_towns_in_England")
# content = driver.page_source
# soup = BeautifulSoup(content)
