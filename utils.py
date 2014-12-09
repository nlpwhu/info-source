import requests
from bs4 import BeautifulSoup
from data import COLUMN, EXCLUDE_COLUMN
from string import punctuation

from region_province_map import RegionProvinceMap

import tldextract

# pass in a file, each line indicates a website name,
# by default we assume the first two characters are the location
# if not, we set the location mannually
# 
# example:
# 四平日报
# 大兴安岭日报 1 4

def get_location_info(filename):
    lines = [line.split() for line in open(filename)]
    result = {}
    for item in lines:
        if not item: continue
        
        name = item[0]

        if (len(item) > 1):
            start, end = int(item[1]) - 1, int(item[2])
        else:
            start, end = 0, 2

        location = name[start:end]

        result[name] = dict(location=location, province=get_province(location))
    
    return result

def get_province(region_name):
    return RegionProvinceMap().get_province(region_name)


def get_domain(url):
    if not url:
        return None
    else:
        extracted = tldextract.extract(url)
        return extracted.domain + extracted.suffix if extracted else None

def merge_two_dicts(x, y):
    return dict(list(x.items()) + list(y.items()))
