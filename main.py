#!/usr/bin/python3
#-*-coding:utf-8 -*-

from post import Post
from parser import Parse
from config import USERNAME
import sys

if __name__ == "__main__":

    items = Parse().items

    p = Post()
    
    login_response = p.logon().content.decode("utf-8")

    # if not valid login, exit
    if "我的录入" not in login_response:
        print("login failed")
        exit()

    # start from a specific number
    if sys.argv.__len__() > 1:
        startFrom = int(sys.argv[1])
        f = open('textfiles/intermediate-result.txt', 'a')
    else:
        startFrom = 0
        f = open('textfiles/intermediate-result.txt', 'w+')

    count = startFrom
    total = len(items)
    for item in items[count:]:
        print(count, "/", total)
        print(USERNAME, "posting", item['websiteplate'], item['url'])
        r = p.post(item)
        print(r.content.decode("utf-8"))
        count += 1
        