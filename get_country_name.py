# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import re
import time

import requests
from lxml import etree  

import agents
import mongodb_handler as mh
import journal as jn
import utilities as ut
import message as msg
import stats
import config

def crawl():  # 爬具体页面
    link = "http://www.nationsonline.org/oneworld/countries_of_the_world.htm#A"
    opener = requests.Session() # 新建了session保存
    content = opener.get(link, headers=agents.get_header()).text # 注意，这里是不断随机换agent的
    selector = etree.HTML(content.encode("utf-8"))

    countries = selector.xpath("//table[@class=\"nix\"]//a")
    
    country_set = []
    for country in countries:
        country_set.append(country.xpath('string(.)'))
    return country_set

print crawl()