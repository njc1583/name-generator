#!/usr/bin/python

import sys
import os
import re
import json
import argparse

import generator 

parser = argparse.ArgumentParser(description='Name Generator Argument Parser')

parser.add_argument(
    '--culture',
    type=str,
    default='american',
    help='culture of names you wish to generate'
)
parser.add_argument(
    '--datapath',
    type=str,
    default='city_data',
    help='the data path without JSON extension'
)
parser.add_argument(
    '--quantity',
    type=int,
    default=5,
    help='number of names you wish to generate'
)


args = parser.parse_args()

culture = args.culture.lower()
json_path = args.datapath.lower() + '.json'
quantity = args.quantity

all_data = {}

try:
    with open(json_path, 'r') as f:
        all_data = json.load(f)
except:
    print('ERROR: {} is not a valid datapath'.format(json_path))
    exit()

if culture not in all_data:
    print('ERROR: {} culture is not in the data loaded in'.format(culture))
    exit()

if quantity <= 0:
    print('ERROR: quantity is invalid, setting to default 5')
    quantity = 5

if 'cities' not in all_data[culture]:
    print('ERROR: there are no cities in the culture group {}'.format(culture))
    exit() 

city_data = all_data[culture]
city_list = city_data['cities']

print(city_list)

gen = generator.Generator(culture, city_data)

gen.generate_grammar()
gen.generate_graph()