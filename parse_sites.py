#-*-coding:utf-8 -*-

from utils import get_location_info, merge_two_dicts
from website import WebSite
from data import CAR
import re

def parse_file(filename):
    # newspaper_info = get_location_info(filename)
    # begin to parse file containing paper names, website names and urls
    lines = [line.split() for line in open(filename, encoding = 'utf-8')]
    
    websites = []
    for item in lines:
        if not item: continue

        location, level_name, website_name, url = tuple(item)

        websites.append(dict(location=location, 
                             level_name=level_name, 
                             website_name=website_name, 
                             url=url))

    return websites

 # output:
 #{'铜陵新闻网': {'url': 'http://www.tlnews.cn/', 'province': '安徽省'},
 # '池州新闻网': {'url': 'http://www.chiznews.com/', 'province': '安徽省'},
 # '滁州网': {'url': 'http://www.chuzhou.cn/', 'province': '安徽省'},
 # '常州第一门户网': {'url': 'http://www.cz001.com.cn/', 'province': '江苏省'},
 # '伊春新闻网': {'url': 'http://yichun.dbw.cn/', 'province': '黑龙江省'}}
def to_site_info(newspaper_info):
    site_info = []
    for newspaper in newspaper_info:
        paper = newspaper_info[newspaper]

        if ('province' in paper and 'website_name' in paper and 'url' in paper):
            province = paper['province']
            website_name = paper['website_name']
            url = paper['url']
            site_info.append(dict(province=province, url=url, website_name=website_name))

    return site_info


def get_all_columns(site):
    w = WebSite(site['website_name'], site['url'])
    links = w.valid_links
    result = [[site['location'], site['level_name'], site['website_name'], link.href, link.text] for link in links]
    result.append([site['location'], site['level_name'], site['website_name'], site['url'], "首页"])
    return result

    # site_info = parse_newspaper_file("sitenames.csv")
    # for site in site_info.values()[0:3]:
    #     w = Website(site['website_name'], site['url'])
    #     province = site['province']
    #     columns = w.valid_links

def get_type(website_name, websiteplate, url):
    joint_name = "".join([website_name, websiteplate])
    if '博客' in joint_name:
        return '博客'
    elif any(text in joint_name for text in ['论坛', '社区']) or any(text in url for text in ['forum', 'bbs.']):
        return '社区'
    elif '视频' in joint_name:
        return '视频'
    else:
        return '新闻'

def get_group(website_name, websiteplate):
    joint_name = "".join([website_name, websiteplate])
    if any(text in joint_name for text in CAR):
        return '汽车'
    else:
        return '其他'

# column format: 
# 上海 国内省级 搜狐上海 http://cul.sohu.com/ 文化
def add_type_and_group(column):
    location, level_name, website_name, url, websiteplate = tuple(column)

    type_ = get_type(website_name, websiteplate, url)
    group = get_group(website_name, websiteplate)

    return [location, level_name, group, website_name, type_, url, websiteplate]

def readfile2(filename):
    # extract the line
    lines = [line.split() for line in open(filename)]
    return [add_type_and_group(line) for line in lines]
    
# if __name__ == "__main__":
def Parsesites():
    websites = parse_file("1208.txt")


    f = open('filee', 'w+')

    count = 0
    total = len(websites)
    for s in websites:
        columns = get_all_columns(s)

        print(count, "/", total)
        print("processing", s['url'], s['website_name'])

        for x in columns:
            f.write(" ".join(x) + '\n')
        count += 1

    f.close()


    f = open('raw.csv', 'w+')

    for line in readfile2('filee'):
        f.write(" ".join(line) + '\n')
    f.close()






