# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: data_operate.py
   Description: 处理与影响因子及文章分区相关查询
   Author: Dexter Chen
   Date：2017-09-09
-------------------------------------------------
   Development Note：
   1. 查询杂志的标准缩写
   2. 查询杂志N年内的影响因子
   3. 查询杂志分区信息
   4. 储存并调用已查询过的信息
-------------------------------------------------
   Change Log:
   2018-09-14: 重新复活 
-------------------------------------------------
"""

from __future__ import division # python除法变来变去的，这句必须放开头
import time
import sys
import math
import json
import requests
import re
import csv

reload(sys)
sys.setdefaultencoding('utf8')

headers = {'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Referer': "https://www.ncbi.nlm.nih.gov/pubmed",
           "Connection": "keep-alive",
           "Pragma": "max-age=0",
           "Cache-Control": "no-cache",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, sdch",
           "Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6"
           }

run_type = 1

search_str = {"Name": "Value",
              "searchname": "Nature Protocols",
              "searchissn": "",
              "searchfield": "",
              "searchimpactlow": "",
              "searchimpacthigh": "",
              "searchscitype": "",
              "view": "search",
              "searchcategory1": "",
              "searchcategory2": "",
              "searchjcrkind": "",
              "searchopenaccess": "",
              "searchsort": "relevance"}

# 查找杂志的全名
def search_full_name(journal_name):
    url = "http://www.letpub.com.cn/journalappAjax.php?querytype=autojournal&term=" + \
        journal_name.replace(" ", "+")
    tries = 2
    while(tries > 0):
        try:
            opener = requests.Session()
            doc = opener.get(url, timeout=20, headers=headers).text
            return doc
            break
        except Exception, e:
            if run_type:
                print "  ERROR: No matching journal name"
                print e
            tries -= 0
    
def search_jornal_detail():
    url = "http://www.letpub.com.cn/index.php?page=journalapp&view=search"
    tries = 2
    while(tries > 0):
        try:
            opener = requests.Session()
            doc = opener.post(url, data = search_str).text
            print doc
            break
        except expression as identifier:
            pass
            tries -= 0

if __name__ == '__main__':
    # search_jornal_detail()
    print search_full_name("NAT PROTOC")
    
