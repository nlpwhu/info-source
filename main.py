#!/usr/bin/python3
#-*-coding:utf-8 -*-

from post import Post
from parser import Parse
from config import USERNAME

if __name__ == "__main__":

    items = Parse().items

    p = Post()
    
    login_response = p.logon().content.decode("utf-8")

    # if not valid login, exit
    if "我的录入" not in login_response:
        print("login failed")
        exit()

    total = len(items)
    count = 0
    for item in items:
        print(count, "/", total)
        print(USERNAME, "posting", item['websiteplate'], item['url'])
        r = p.post(item)
        print(r.content.decode("utf-8"))
        count += 1
        