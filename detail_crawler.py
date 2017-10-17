# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: detail_crawler.py
   Description: 蜘蛛类，只爬pubmed的详细页
   Author: Dexter Chen
   Date：2017-10-10
-------------------------------------------------
"""

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
import dictionary


def crawl_detail(pmid, proxy=None):  # 爬具体页面   
    link = "https://www.ncbi.nlm.nih.gov/pubmed/" + str(pmid)

    tries = 1  # 尝试获取3次，不成功就返回错误
    while(tries > 0):
        try:
            opener = requests.Session() # 新建了session保存
            content = opener.get(link, timeout=config.request_time_out, headers=agents.get_header()).text # 注意，这里是不断随机换agent的
            selector = etree.HTML(content.encode("utf-8"))

            title_element = selector.xpath("//div[@class = \"rprt abstract\"]//h1")
            if len(title_element):
                title = title_element[0].xpath('string(.)')

            author_element = selector.xpath("//div[@class = \"auths\"]//a")
            authors = []
            if len(author_element):
                for author in author_element:
                    authors.append(author.xpath('string(.)'))

            journal_element = selector.xpath("//a[@alsec=\"jour\"]/@title")
            if len(journal_element):
                journal = journal_element[0]
                if journal:
                    journal_detail = jn.journal_detail(journal)
                    ojournal = journal_detail[0]
                    journal_if = journal_detail[1]
                    journal_zone = journal_detail[2]
            
            abstract_element = selector.xpath("//*[@id=\"maincontent\"]/div/div[5]/div/div[4]")
            if len(abstract_element):
                abstract = abstract_element[0].xpath('string(.)')[8:]

            key_words_element = selector.xpath("//*[@id=\"maincontent\"]/div/div[5]/div/div[5]/p")
            if len(key_words_element):
                key_words = key_words_element[0].xpath('string(.)').split("; ")
            else:
                key_words = []

            issue_element = selector.xpath("//div[@class = \"cit\"]") # 年份
            if len(issue_element):
                issue_raw = issue_element[0].xpath('string(.)')
                issue_start = issue_raw.find(".")
                issue = issue_raw[issue_start + 2:issue_start + 6]

            institues_element = selector.xpath("//div[@class=\"afflist\"]//dd")
            institues = []
            countries = []
            if len(institues_element):
                for institue in institues_element:
                    institues.append(institue.xpath('string(.)'))
                    institue_name = institue.xpath('string(.)')
                    country = institue_name.split(", ")[-1].replace(".","") # 定位最后一个单词（国家）
                    if country not in countries:
                        if country in dictionary.country_name:
                            countries.append(country)


            flink_element = selector.xpath("//div[@class=\"icons portlet\"]//a/@href")
            flinks = []
            if len(flink_element):
                for flink in flink_element:
                    flinks.append(flink)
            

            mh.add_new_content(pmid, title, authors, journal, ojournal, journal_if, journal_zone, issue, abstract, key_words, institues, countries, flinks)
            msg.log("", "2017-10-10 10:10:10", "added", "debug")

            break
        
        except Exception, e:
            tries -= 1
            time.sleep(config.request_refresh_wait)  # 如果抓不成功，就先休息3秒钟
    
    else:
        print "error"
        return 0

if __name__ == '__main__':
    crawl_detail(29027110)