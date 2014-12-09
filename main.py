#!/usr/bin/python3
#-*-coding:utf-8 -*-

from post import Post
from parsers import Parse
from config import USERNAME 
from parse_sites import Parsesites


if __name__ == "__main__":

    Parsesites()
    items = Parse().items

    p = Post()
    
    login_response = p.logon().content.decode("utf-8")

    # if not valid login, exit
    if "我的录入" not in login_response:
        print("login failed")
        exit()

    # total = len(items)
    # count = 2976
    for item in items:
        # print(count, "/", total)
        print(USERNAME, "posting", item['websiteplate'], item['url'])
        r = p.post(item)
        print(r.content.decode("utf-8"))
        # count += 1
        