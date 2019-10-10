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

parser.add_argument(
    '--chromedriver', 
    type=str,
    default='C:/Executables/chromedriver/chromedriver.exe', 
    help='location of chromedriver executable'
)
parser.add_argument(
    '--culture',
    nargs='+',
    type=str,
    default=['english'], 
    help='label for the cultural group you want to scrape'
)
parser.add_argument(
    '--url', 
    nargs='+',
    type=str,
    default=['https://en.wikipedia.org/wiki/List_of_towns_in_England'], 
    help='URL for page you wish to scrape'
)
parser.add_argument(
    '--overwrite',
    type=bool,  
    default=False,
    help='true overwrites all data in city_info.json'
)

args = parser.parse_args()

# print(args)

chromedriver_executable_path = args.chromedriver 
culture_labels = args.culture
wiki_urls = args.url 
overwrite = args.overwrite 
json_path = 'city_data.json'

try:
    with open(json_path, 'r') as f:
        city_data = json.load(f)
except:
    city_data = {}

driver = webdriver.Chrome(executable_path=chromedriver_executable_path)

for i in range(min(len(culture_labels), len(wiki_urls))):
    wiki_url = wiki_urls[i]
    culture_label = culture_labels[i]

    driver.get(wiki_url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    tables = soup.findAll('table', attrs={'class': 'wikitable sortable jquery-tablesorter'})

    if overwrite or culture_label not in city_data:
        city_data[culture_label] = {'cities': [], 'sources': []}

    if wiki_url not in city_data[culture_label]['sources']:
        city_data[culture_label]['sources'].append(wiki_url)

    title_regex = re.compile('.+')

    for table in tables:
        for td_href in table.find_all('a', href=True, attrs={'title': title_regex}):
            city_name = td_href.text

            if city_name not in city_data[culture_label]['cities']:
                city_data[culture_label]['cities'].append(city_name)

    if len(city_data[culture_label]) == 0:
            print("ERROR: Could not properly parse city names")
            del(city_data[culture_label])

driver.quit()

with open(json_path, 'w', encoding='utf-8') as outfile:
    json.dump(city_data, outfile, indent=4, ensure_ascii=False)