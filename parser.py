#!/usr/bin/python3
#-*-coding:utf-8 -*-

from data import REGION, TYPE, LEVEL, GROUP
from allRegions import ALL_REGIONS
from config import FILENAME

class Parse:
    def __init__(self):
        self.read_file()
        self.add_all()
        self.del_redundant()

    def read_file(self):
        lines = [line.split() for line in open(FILENAME)]
        self.items = []
        for item in lines:
            if not item: continue # skip empty line

            new_item = dict(location   = item[0],
                            level_name = item[1],
                            group_name = item[2],
                            website    = item[3], 
                            category   = item[4], 
                            url        = item[5])

            # get the string of websiteplate
            # example: 南阳新闻网_财经
            # if there is no content here, set to websitename_首页
            websitename = item[3:4]
            if (len(item) > 6):
                websiteplate = '_'.join(websitename + item[6:])
            else:
                websiteplate = '_'.join(websitename + ['首页'])

            # set the field to the dict
            new_item['websiteplate'] = websiteplate

            # add to list
            self.items.append(new_item)

        '''
        so that the format of items is
        [{'location': '河南',
          'level_name'国内地方',
          'category': '新闻',
          'website': '南阳新闻网',
          'url': 'http://epaper.01ny.cn/',
          'websiteplate': '南阳新闻网_首页'},...]
        '''

    # check whether the first two characters of two strings match or not
    def match_first_two_chars(self, str1, str2):
        return str1[0:2] == str2[0:2]

    def exact_match(self, x, y): 
        return x == y

    # search for an item
    def search(self, field, target, source, match_fun):
        res = [item for item in source if match_fun(item[field], target)]

        if res:
            return res[0]
        else:
            print(target ,"No Match or There is another same name city")
            return None

    # add region name and region id to the items
    def add_region(self, item):
        region = self.search('regionname', item['location'], ALL_REGIONS, self.exact_match)
        item.update(region)

    # add type to the items
    def add_type(self, item):
        _type = self.search('name', item['category'], TYPE, self.exact_match)
        item.update(_type)

    # add level to the items
    def add_level(self, item):
        level = self.search('name', item['level_name'], LEVEL, self.exact_match)
        item.update(level) 

    # add group to the items
    def add_group(self, item):
        group = self.search('name', item['group_name'], GROUP, self.exact_match)
        item.update(group)

    # add
    def add_all(self):
        for item in self.items:
            self.add_region(item)
            self.add_type(item)
            self.add_level(item)
            self.add_group(item)

    # delete redundant fields
    def del_redundant(self):
        for item in self.items:
            item.pop('name', None)
            item.pop('location', None)
