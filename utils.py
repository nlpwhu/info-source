import requests
from bs4 import BeautifulSoup
from data import COLUMN, EXCLUDE_COLUMN
from string import punctuation

import all_regions

import tldextract

# pass in a file, each line indicates a website name,
# by default we assume the first two characters are the location
# if not, we set the location mannually
# 
# example:
# 四平日报
# 大兴安岭日报 1 4

def get_location(filename):
    lines = [line.split() for line in open(filename)]
    items = []
    for item in lines:
        if not item: continue
        
        name = item[0]

        if (len(item) > 1):
            start, end = int(item[1]) - 1, int(item[2])
        else:
            start, end = 0, 2

        location = name[start:end]

        items.append(dict(name=name, location=location))
    
    return items


def get_region(location_list):
    # cities = all_regions.cities
    # def has_location(district):
    #     return district['name'] == location or 
    # find the location in the dict
    pass

def get_domain(url):
    if not url:
        return None
    else:
        extracted = tldextract.extract(url)
        return extracted.domain + extracted.suffix if extracted else None

