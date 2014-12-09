#-*-coding:utf-8 -*-

from utils import get_location_info, merge_two_dicts
from website import WebSite
from data import CAR
import re

def parse_file(filename):
    # newspaper_info = get_location_info(filename)
    # begin to parse file containing paper names, website names and urls
    lines = [line.split() for line in open(filename)]
    
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
    
if __name__ == "__main__":
    websites = parse_file("textfiles/1208.txt")
    # f = open('filee', 'a+')

    # count = 53
    # total = len(websites)
    # for s in websites[53:]:
    #     columns = get_all_columns(s)
    #     print(count, "/", total)
    #     print("processing", s['url'], s['website_name'])
    # # s = [['山东省', '东方圣城网', 'http://www.jn001.com/travel/2014-05/12/content_3115.htm', '邹城市峄山'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_116.htm', '太白湖'], ['山东省', '东方圣城网', 'http://www.jn001.com/finance/node_150.htm', '财富聚焦'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/gzrjwh.htm', '儒学'], ['山东省', '东方圣城网', 'http://www.jn001.com/health/', '健康'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel', '旅游'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_168.htm', '济宁特产'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_105.htm', '时政要闻'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_106.htm', '县区'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_110.htm', '视频'], ['山东省', '东方圣城网', 'http://www.jn001.com/house/node_147.htm', '楼市资讯'], ['山东省', '东方圣城网', 'http://bbs.jn001.com', '论坛'], ['山东省', '东方圣城网', 'http://www.jn001.com/finance', '财经'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/skyx.htm', '三孔映像'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/2014-05/12/content_3121.htm', '羊山度假区'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/gzrjwh.htm', '儒家文化'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/2014-09/26/content_46093.htm', '南阳古镇'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_124.htm', '梁山'], ['山东省', '东方圣城网', 'http://www.jn001.com/finance/node_149.htm', '保险资讯'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_285.htm', '国学文化'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_103.htm', '今日时评'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_117.htm', '高新区'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture', '三孔'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_237.htm', '文化名人'], ['山东省', '东方圣城网', 'http://house.jn001.com/', '房产交易'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_121.htm', '泗水'], ['山东省', '东方圣城网', 'http://www.jn001.com/auto/node_155.htm', '车商资讯'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_169.htm', '景点推介'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_173.htm', '城市风光'], ['山东省', '东方圣城网', 'http://www.jn001.com/finance/node_153.htm', '财经访谈'], ['山东省', '东方圣城网', 'http://www.jn001.com/house/node_144.htm', '榜样空间'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_170.htm', '美食'], ['山东省', '东方圣城网', 'http://www.jn001.com/auto/node_155.htm', '汽车生活'], ['山东省', '东方圣城网', 'http://www.jn001.com/house/node_142.htm', '高端楼盘'], ['山东省', '东方圣城网', 'http://car.jn001.com/', '汽车'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_170.htm', '济宁美食'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_118.htm', '嘉祥'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_179.htm', '运河文化'], ['山东省', '东方圣城网', 'http://www.jn001.com/finance/node_241.htm', '财经济宁'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_168.htm', '特产'], ['山东省', '东方圣城网', 'http://www.jn001.com/auto/node_158.htm', '济宁车市'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_178.htm', '微湖风情'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_122.htm', '汶上'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_103.htm', '济宁经济'], ['山东省', '东方圣城网', 'http://bbs.jn001.com/', '济宁论坛'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture', '文化'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_127.htm', '任城'], ['山东省', '东方圣城网', 'http://www.jn001.com/auto/node_159.htm', '专业评测'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_111.htm', '精彩专题'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_285.htm', '水浒'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_280.htm', '运河'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_119.htm', '鱼台'], ['山东省', '东方圣城网', 'http://www.jn001.com/house/node_145.htm', '济宁地产'], ['山东省', '东方圣城网', 'http://house.jn001.com/newhouse/zz/3.html', '太白国际'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_126.htm', '兖州'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_125.htm', '曲阜'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/fdws.htm', '佛都汶上'], ['山东省', '东方圣城网', 'http://www.jn001.com/house/node_143.htm', '地产名人'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_182.htm', '佛教文化'], ['山东省', '东方圣城网', 'http://house.jn001.com/newhouse/zz/3.html', '详细'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_120.htm', '微山'], ['山东省', '东方圣城网', 'http://house.jn001.com/', '房产'], ['山东省', '东方圣城网', 'http://www.jn001.com/culture/node_236.htm', '感知济宁'], ['山东省', '东方圣城网', 'http://www.jn001.com/index/node_274.htm', '济宁风光'], ['山东省', '东方圣城网', 'http://www.jn001.com/health/node_164.htm', '养生'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_123.htm', '金乡'], ['山东省', '东方圣城网', 'http://www.jn001.com/travel/node_994.htm', '微湖风情'], ['山东省', '东方圣城网', 'http://www.jn001.com/news/node_115.htm', '邹城']]
    #     for x in columns:
    #         f.write(" ".join(x) + '\n')
    #     count += 1
    # f.close()


    f = open('fileee', 'w+')

    for line in readfile2('filee'):
        f.write(" ".join(line) + '\n')
    f.close()






