# -*- coding: utf-8 -*-
# !/usr/bin/env python

import requests
from lxml import etree
import config
import agents

def crawl_name():  # 爬具体页面
    link = "https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations"
    opener = requests.Session()  # 新建了session保存
    content = opener.get(link, timeout=config.request_time_out,
                            headers=agents.get_header()).text  # 注意，这里是不断随机换agent的
    selector = etree.HTML(content.encode("utf-8"))
    name_element = selector.xpath("//*[@id=\"bodyContent\"]//table//tr/td//span")

    print len(name_element)
    for item in name_element:
        print item.xpath('string(.)')


crawl_name()
