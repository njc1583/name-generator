#!/usr/bin/python

import sys
import os
import re
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import pandas as pd 
import argparse

parser = argparse.ArgumentParser(description='Web Scraper Argument Parser')

parser.add_argument('--chromedriver', default='C:/Executables/chromedriver/chromedriver.exe', type=str, help='location of chromedriver executable')
parser.add_argument('--culture', default='english', type=str, help='label for the cultural group you want to scrape')
parser.add_argument('--url', default='https://en.wikipedia.org/wiki/List_of_towns_in_England', type=str, help='URL for page you wish to scrape')
parser.add_argument('--overwrite', default=False, type=bool, help='true overwrites all data in city_info.json')

args = parser.parse_args()

# print(args)

chromedriver_executable_path = args.chromedriver 
culture_label = args.culture
wiki_url = args.url 
overwrite = args.overwrite 
json_path = 'city_data.json'

try:
    with open(json_path, 'r') as f:
        city_data = json.load(f)
except:
    city_data = {}

driver = webdriver.Chrome(executable_path=chromedriver_executable_path)

driver.get(wiki_url)

content = driver.page_source
soup = BeautifulSoup(content)

tables = soup.findAll('table', attrs={'class': 'wikitable sortable jquery-tablesorter'})

if overwrite or culture_label not in city_data:
    city_data[culture_label] = []

title_regex = re.compile('.+')

for table in tables:
    for td_href in table.find_all('a', href=True, attrs={'title': title_regex}):
        city_name = td_href.text

        if city_name not in city_data[culture_label]:
            city_data[culture_label].append(city_name)

driver.quit()

with open(json_path, 'w') as outfile:
    json.dump(city_data, outfile, indent=4)