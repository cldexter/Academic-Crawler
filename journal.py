# -*- coding: utf-8 -*-
# !/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------
   File Name: journal.py
   Description: 处理与影响因子及文章分区相关查询
   Author: Dexter Chen
   Date：2017-09-09
-------------------------------------------------
   Development Note：
   1. 查询杂志的标准缩写, 支持非完整查询
   2. 查询杂志最后一次有记录的影响因子
   3. 查询杂志分区信息
   4. 储存并调用已查询过的信息，不用反复联网，增加速度
-------------------------------------------------
   Change Log:
   2017-09-14: 重新复活
   2017-09-15: 自动判断是否已搜索过
-------------------------------------------------
"""

from __future__ import division  # python除法变来变去的，这句必须放开头
import sys
import re
import requests
from BeautifulSoup import BeautifulSoup
from data_handler import csv_write, csv_read

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

run_type = 0


def search_full_name(journal_name):  # 查找杂志的全名，支持模糊查询，只输出最符合的那个
    url = "http://www.letpub.com.cn/journalappAjax.php?querytype=autojournal&term=" + \
        journal_name.replace(" ", "+")
    try:
        opener = requests.Session()
        doc = opener.get(url, timeout=20, headers=headers).text
        list = doc.split('},{')
        journal_name_start = list[0].find("label") + 8
        journal_name_end = list[0].find("\",\"", journal_name_start)
        journal_name = list[0][journal_name_start:journal_name_end]
        if run_type:
            print "  INFO: Journal full name retrieved from LetPub."
            print list
            print "Journal Name: " + journal_name
        return journal_name
    except Exception, e:
        if run_type:
            print "  ERROR: No matching journal name found on LetPub."
            print e
        return "No Record"

def search_jornal_detail(journal_full_name):# 查找杂志影响因子、分区, 要求输入精准
    url = "http://www.letpub.com.cn/index.php?page=journalapp&view=search"
    search_str = {
        "searchname":"",
        "searchissn":"",
        "searchfield":"",
        "searchimpactlow":"",
        "searchimpacthigh":"",
        "searchscitype":"",
        "view": "search",
        "searchcategory1":"",
        "searchcategory2":"",
        "searchjcrkind":"",
        "searchopenaccess":"",
        "searchsort": "relevance"}
    search_str["searchname"] = journal_full_name
    try:
        opener = requests.Session()
        doc = opener.post(url, data=search_str).text
        soup = BeautifulSoup(doc)
        table = soup.findAll(name="td", attrs={
                                "style": "border:1px #DDD solid; border-collapse:collapse; text-align:left; padding:8px 8px 8px 8px;"})

        re_label = re.compile("</?\w+[^>]*>")
        text = re_label.sub("", str(table)).split(', ')
        impact_factor = text[2]
        publication_zone = text[3][0]
        if run_type:
            print "  INFO: Journal information retrieved from LetPub."
        return impact_factor, publication_zone
    except Exception, e:
        if run_type:
            print "  ERROR: No journal detail retrieved from LetPub."
            print e
        return "",""

def journal_detail(journal_name): # 使用使用的函数，自带储存功能
    journal_full_name = search_full_name(journal_name)
    journal_record = csv_read("universal","journal")
    for journal in journal_record:
        if journal.split(",")[0] == journal_full_name:
            data = journal.split(",")
            if run_type:
                print "  INFO: Journal information retrieved from local."
            return data
    else:
        journal_detail = search_jornal_detail(journal_full_name)
        journal_IF = journal_detail[0]
        journal_zone = journal_detail[1]
        data = journal_full_name, journal_IF, journal_zone
        csv_write(data,"universal","journal")
        return data

if __name__ == '__main__':
    print journal_detail("journal of food microbiology")