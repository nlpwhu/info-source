#-*-coding:utf-8 -*-
from all_regions import REGIONS

class RegionProvinceMap:
    def __init__(self):
        self.region_province_map=dict()
        self.load_province_list(REGIONS)

    def load_province_region(self, province_name, sub):
        for obj in sub:
            self.region_province_map[obj['name']]=province_name
            if ('sub' in obj):
                self.load_province_region(province_name,obj['sub'])

    def load_province_list(self, province_list):
        for province in province_list:
            province_name = province['name']
            sub = province['sub']
            self.load_province_region(province_name, sub)

    def get_province(self, region_name):
        matched_key = [r for r in self.region_province_map if r.startswith(region_name)]
        if matched_key:
            return self.region_province_map[matched_key[0]]
        else:
            return "Unknown"
