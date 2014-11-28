#-*-coding:utf-8 -*-

import requests
import re
from functools import reduce

from bs4 import BeautifulSoup
from data import COLUMN, EXCLUDE_COLUMN
from region_name import REGION_NAME
from string import punctuation

from utils import get_domain

from urllib.parse import urlsplit

PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~［］'

# pass in a file, each line indicates a website name,
# by default we assume the first two characters are the location
# if not, we set the location mannually
# 
# example:
# 四平日报
# 大兴安岭日报 1 4
class WebSite:
    def __init__(self, name, url):
        self.name = name
        # self.url = url 
        self.url = url.replace(' ','')  
        self.html = self.get_html()
        self.domain = get_domain(self.url) # e.g. stackoverflow.com
        self.base_url = self.get_base_url() # e.g. http://stackoverflow.com/
        self.all_links = self.get_all_links()
        self.some_valid_links = self.get_some_valid_links()

        self.valid_links = self.get_all_valid_links()


    def get_base_url(self):
        return "{0.scheme}://{0.netloc}/".format(urlsplit(self.url))

    def get_html(self):
        r = requests.get(self.url)
        html = BeautifulSoup(r.content, from_encoding='GB18030')
        return html

    def get_all_links(self):
        links = {Link(link, self.base_url) for link in self.html.find_all('a')}
        return links

    # fetch some valid links according to the COLUMN set first,
    # we will try to get more later
    def get_some_valid_links(self):
        some_valid_links = {link for link in self.all_links 
                            if (link.valid() and
                                link.name_not_in_excluded_set() and
                                link.name_in_column_set() or
                                link.name_is_location())}
        return some_valid_links


    def get_all_valid_links(self):
        some_valid_links = self.get_some_valid_links()
        all_siblings = self.get_all_siblings()
        links = set.union(some_valid_links, all_siblings)
        return {link for link in links 
                if link.same_domain(self) and link.name_not_in_excluded_set()}
  
    def get_all_siblings(self):
        return reduce(lambda x, y: x.union(y.siblings()), self.some_valid_links, set())


class Link:
    def __init__(self, link, base_url):
        self.text = self.get_text(link)
        self.class_ = self.get_class(link)
        self.href = self.get_href(link, base_url)
        self.domain = get_domain(self.href)
        self.parent = link.parent
        self.base_url = base_url

    def __repr__(self):
        text = self.text if self.text else "wtf empty??"
        class_ = str(self.class_) if self.class_ else ""
        href = self.href if self.href else ""
        return " ".join([text, class_, href])

    def __eq__(self, other):
        if isinstance(other, Link):
            return (self.text == other.text and 
                    self.href == other.href and
                    self.parent == self.parent and
                    self.class_ == other.class_)
        else:
            return False

    def __hash__(self):
        class_ = self.class_ if self.class_ else []
        return hash( (self.text, self.href, tuple(class_)) )

    def get_text(self, link):
        return re.sub(r'[\s\u3000>·】【\[\]]', r'', link.text)

    def get_same_class_links(self, links):
        # if link has class attribute and is not " "(space)
        if self.class_:
            return [l for l in self.links if l._class == link._class]
        else:
            return []

    def get_class(self, link):
        # has class and not all blank
        class_ = link.get('class')

        if class_ and "".join(class_).strip():
            return [c for c in class_ if c] # remove empty strings
        else: 
            return None
    
    def get_href(self, link, base_url):
        href = link.get('href')
        if (not href) or ('http://' in href) or ('https://' in href):
            return href
        elif ('//' in href):   
            return None
        elif (href.startswith('/')):
            return base_url[:-1] + href
        else:
            return base_url + href

    def href_valid(self):
        # condition: not None and not blank and not '#' and not javascript code
        return bool((self.href and
                     self.href.strip() and
                     '#' not in self.href.strip() and
                     'javascript:' not in self.href.lower()))

    # this function indicates if the link name is valid
    # as a column name
    # prerequisite:
    # 1. length < 4 or length < 2 (1 or 0)
    # 2. not having punctuation in the name
    # 3. name is not excluded
    # 4. name is in the column name set
    def name_valid(self):
        name = self.text
        if (len(name) > 5 or
            len(name.strip()) < 2 or
            any(p in name for p in PUNCTUATION)):
            # any(column in name for column in EXCLUDE_COLUMN)): # name is excluded
            return False
        else:       
            return True

    def valid(self):
        return self.href_valid() and self.name_valid()

    def name_is_location(self):
        is_location = (self.text.endswith(('市','县','区','镇','村','乡')) or
                       any(self.text in column for column in REGION_NAME))
        return self.name_valid() and self.href_valid() and is_location

    def name_in_column_set(self):
        # return if there is a column that its name is contained
        # in the name given
        return any(column in self.text for column in COLUMN)

    def name_not_in_excluded_set(self):
        name = self.text
        return all(column not in name for column in EXCLUDE_COLUMN)

    def same_domain(self, website):
        return self.domain in website.domain if self.domain else False

    def siblings(self):
        ancestor = self.parent
        while(len(ancestor.find_all('a')) < 2):
            ancestor = ancestor.parent

        siblings = {Link(link, self.base_url) for link in ancestor.find_all('a')}

        # if there is any invalid link in the siblings set,
        # discard the sibling set
        if all(link.valid() for link in siblings):
            return siblings
        else:
            return set()