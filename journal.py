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
   1. 清洗杂志名称，去除解释、说明等
   2. 查询杂志的标准缩写, 支持非完整查询
   3. 储存并调用已查询过的信息，增加速度
   4. 如数据库中没有，查询杂志最后一次有记录的影响因子
   5. 如数据库中没有，查询杂志分区信息
   6. 储存新杂志信息
-------------------------------------------------
   Change Log:
   2017-09-15: 自动判断是否已搜索过
   2017-10-01: 大幅优化；自动清洗杂志名称
-------------------------------------------------
"""

from __future__ import division  # python除法变来变去的，这句必须放开头
import sys
import re
import requests
from BeautifulSoup import BeautifulSoup

import mongodb_handler as mh
import agents
from data_handler import csv_write, csv_read

reload(sys)
sys.setdefaultencoding('utf8')

run_type = 0


def text_wash(journal_name):  # 原始名称清洗（主要针对各种括号和标点、解释、注释）
    re_bracket = re.compile("[\\[\\(](.*?)[\\]\\)]")
    re_explaination = re.compile(" ??[:=].*")
    journal_name = journal_name.replace('&amp;',"&").replace(',','')
    journal_name = re_bracket.sub('', journal_name)
    journal_name = re_explaination.sub('', journal_name)
    if run_type:
        print "  INFO: Journal name cleaned."
        print "  Journal Name: " + journal_name.upper()
    return journal_name.upper() # 清洗过的名称全大写

def get_full_name(journal_name):  # 查找杂志的全名，支持模糊查询，只输出最符合的那个
    url = "http://www.letpub.com.cn/journalappAjax.php?querytype=autojournal&term=" + journal_name.replace("&","%26").replace(" ", "+")
    try:
        opener = requests.Session()
        doc = opener.get(url, timeout=20, headers=agents.get_header()).text
        list = doc.split('},{') # 获取列表，但是只有最match的被采纳
        journal_name_start = list[0].find("label") + 8
        journal_name_end = list[0].find("\",\"", journal_name_start)
        journal_name = list[0][journal_name_start:journal_name_end]
        if run_type:
            print "  URL:" + url
            print "  INFO: Journal full name retrieved from LetPub."
            print list
            print "  Journal Name: " + journal_name
        return journal_name
    except Exception, e:
        if run_type:
            print "  ERROR: No matching journal name found on LetPub."
            print e
        return ""

def get_jornal_if(journal_official_name):# 查找杂志影响因子、分区, 要求输入精准
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
    search_str["searchname"] = journal_official_name
    try:
        opener = requests.Session()
        doc = opener.post(url, timeout=20, data=search_str).text
        soup = BeautifulSoup(doc)
        table = soup.findAll(name="td", attrs={
                                "style": "border:1px #DDD solid; border-collapse:collapse; text-align:left; padding:8px 8px 8px 8px;"})

        re_label = re.compile("</?\w+[^>]*>")
        text = re_label.sub("", str(table)).split(', ')
        impact_factor = text[2] # 影响因子
        publication_zone = text[3][0] # 文章分区，只有第一个数字被截取
        if run_type:
            print "  INFO: Journal information retrieved from LetPub."
        return impact_factor, publication_zone
    except Exception, e:
        if run_type:
            print "  ERROR: No journal detail retrieved from LetPub."
            print e
        return "",""

def journal_detail(journal_name): # 使用使用的函数，自带储存功能
    journal_name = text_wash(journal_name) # 清洗文本，大写
    journal_official_name = get_full_name(journal_name) # 输入模糊名，输出精准名
    journal_record = mh.read_journal_name_all() 
    if journal_official_name in journal_record: # 如果数据库中已经有了
        record = mh.read_journal_detail(journal_official_name) # 直接提取
        if run_type:
            print "  INFO: Journal information retrieved from local."
        return record
    else:
        journal_detail = get_jornal_if(journal_official_name)
        journal_if = journal_detail[0]
        journal_zone = journal_detail[1]
        data = journal_official_name, journal_if, journal_zone
        mh.add_journal(journal_official_name, journal_if, journal_zone) # 注意只储存大写
        return data

if __name__ == '__main__':
    print journal_detail("Clinical advances in hematology &amp; oncology : H&amp;O")
    # print journal_detail("Clinical &amp; experimental metastasis")
    # print journal_detail('cancer epidemiology biomarkers & prevention')
