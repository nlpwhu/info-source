#-*-coding:utf-8 -*-


import requests
import re
from functools import reduce

from bs4 import BeautifulSoup
from data import COLUMN, EXCLUDE_COLUMN
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
        self.url = url
        self.html = self.get_html()
        self.domain = get_domain(self.url) # e.g. stackoverflow.com
        self.base_url = self.get_base_url() # e.g. http://stackoverflow.com/
        self.all_links = self.get_all_links()
        self.some_valid_links = self.get_some_valid_links()

        self.valid_links = self.get_all_valid_links()
        # self.add_same_class_links()
        # self.nav_links = self.get_nav_links()
        # self.all_siblings = self.get_all_siblings()

        self.excluded_class = set()


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
                            if (link.valid() and link.name_in_column_set())}
        return some_valid_links


    def get_all_valid_links(self):
        some_valid_links = self.get_some_valid_links()
        same_class_links = self.get_all_same_class()
        # all_siblings = self.get_all_siblings()
        # return set(filter((lambda link: link.same_domain(self)),
        #                    some_valid_links.union(same_class_links)
        #                                    .union(all_siblings)))
        return set(filter((lambda link: link.same_domain(self)),
                           some_valid_links.union(same_class_links)))

    
    def extract_links_from_divs(self, divs):
        # links = [div.find_all('a') for div in divs]
        # # add links together, if no result, return empty list
        # links = reduce(lambda x, y: x + y, links) if links else []
        # links = {Link(link, self.base_url) for link in links}
        # links = {link for link in links if link.valid() and link.same_domain(self)}

        # return links

        # pass in a list of links, check if all links satisfy the prerequisite
        def links_all_valid(links,div):
            for link in links:
                if not (link.valid() and link.same_domain(self)):
                    return False
            return True

        # return set(filter (lambda links: links_all_valid(links),
        #                 map (lambda link: Link(link, self.base_url),
        #                     map (lambda div: div.find_all('a'),
        #                          divs))))

        result = set()
        explored = set()
        for div in divs:
            links = div.find_all('a') # a list of links
            links = (Link(link, self.base_url) for link in links) # a tuple of Links
            if links in explored:
                continue
            elif (links_all_valid(links, div)):
                explored.update(set(links))
                result.update(set(links))
            else: # invalid
                if (div.get('class')):
                    self.excluded_class.update(tuple(div.get('class')))
                return set()

        return result

    def get_nav_links(self):
        # find divs that have 'nav' in the class name
        divs = self.html.find_all("div", {"class" : re.compile('.*nav.*')})
        return self.extract_links_from_divs(divs)

    def get_siblings(self, link):
        ancestor_having_class = link.parent

        while (not ancestor_having_class.get('class')):
            ancestor_having_class = ancestor_having_class.parent

        class_ = ancestor_having_class.get('class')

        # the class name has already been visited and also excluded
        if tuple(class_) in self.excluded_class:
            return set()
        else:
            divs = self.html.find_all(class_=class_)
            return self.extract_links_from_divs(divs)

    # there are some links not in the COLUMN set,
    # but still should be recorded
    # so we iterate the links, find the links that have the same class
    def get_same_class_links(self, link):
        if not link.class_:
            return set() 
        else:
            divs = self.html.find_all(class_=link.class_)
            return self.extract_links_from_divs(divs)

    def get_all_siblings(self):
        return reduce(lambda x, y: x.union(self.get_siblings(y)), self.some_valid_links, set())
        
    def get_all_same_class(self):
        return reduce(lambda x, y: x.union(self.get_same_class_links(y)), self.some_valid_links, set())


class Link:
    def __init__(self, link, base_url):
        self.text = self.get_text(link)
        self.class_ = self.get_class(link)
        self.href = self.get_href(link, base_url)
        self.domain = get_domain(self.href)
        self.parent = link.parent

    def __repr__(self):
        text = self.text if self.text else "wtf empty??"
        class_ = str(self.class_) if self.class_ else ""
        href = self.href if self.href else ""
        return " ".join([text, class_, href])

    def __eq__(self, other):
        if isinstance(other, Link):
            return self.text == other.text and self.href == other.href
        else:
            return False

    def __hash__(self):
        return hash( (self.text, self.href) )

    def get_text(self, link):
        return re.sub(r'[\s\u3000]', r'', link.text)

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
        if (len(name) > 4 or
            len(name.strip()) < 2 or
            any(p in name for p in PUNCTUATION) or # has_punctuation
            any(column in name for column in EXCLUDE_COLUMN)): # name is excluded
            return False
        else:
            return True

    def valid(self):
        return self.href_valid() and self.name_valid()

    def name_in_column_set(self):
        # return if there is a column that its name is contained
        # in the name given
        return any(column in self.text for column in COLUMN)

    def same_domain(self, website):
        return self.domain in website.domain if self.domain else False
