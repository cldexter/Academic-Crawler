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
from multiprocessing import Pool

import agents
import mongodb_handler as mh
import journal as jn
import utilities as ut
import message as msg
import stats
import config
import dictionary


def get_pmid_list(project, sstr, pmid_number):
    pmid_list = mh.read_empty_pmid(project, sstr, pmid_number)
    return pmid_list


def crawl_detail(pmid, proxy=None):  # 爬具体页面
    link = "https://www.ncbi.nlm.nih.gov/pubmed/" + str(pmid)
    tries = config.request_dp_tries  # 根据设定重复次数
    msg.msg("record", pmid, "retrieved", "proc", "info", msg.display, msg.stat)
    while(tries > 0):
        try:
            authors = []
            institues = []
            countries = []
            flinks = []
            opener = requests.Session()  # 新建了session保存
            content = opener.get(link, timeout=config.request_time_out,
                                 headers=agents.get_header()).text  # 注意，这里是不断随机换agent的
            selector = etree.HTML(content.encode("utf-8"))
            title_element = selector.xpath(
                "//div[@class = \"rprt abstract\"]//h1")
            if len(title_element):
                title = title_element[0].xpath('string(.)')
            author_element = selector.xpath("//div[@class = \"auths\"]//a")
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
            abstract_element = selector.xpath(
                "//*[@id=\"maincontent\"]/div/div[5]/div/div[4]")
            if len(abstract_element):
                abstract = abstract_element[0].xpath('string(.)')[8:]
            key_words_element = selector.xpath(
                "//*[@id=\"maincontent\"]/div/div[5]/div/div[5]/p")
            if len(key_words_element):
                key_words = key_words_element[0].xpath('string(.)').split("; ")
            else:
                key_words = []
            issue_element = selector.xpath("//div[@class = \"cit\"]")  # 年份
            if len(issue_element):
                issue_raw = issue_element[0].xpath('string(.)')
                issue_start = issue_raw.find(".")
                issue = issue_raw[issue_start + 2:issue_start + 6]
            institues_element = selector.xpath("//div[@class=\"afflist\"]//dd")
            if len(institues_element):
                for institue in institues_element:
                    institue = institue.xpath('string(.)')
                    institue = ut.regexp_replace(
                        institue, ut.re_email_pm)  # 去除pm的email语句
                    institue = ut.regexp_replace(
                        institue, ut.re_email_general)  # 去除所有中间的email
                    institue = institue.replace(" ,", ",")
                    institues.append(institue)
                    institue = institue.replace(", ", ",").replace(".", "")
                    institue_strs = institue.split(",")
                    institue_strs.reverse() # 国家名往往放在最后
                    i = 0
                    while i < len(institue_strs):
                        if institue_strs[i] in dictionary.country_names.keys(): # 如果有这个机构
                            country_name = dictionary.country_names[institue_strs[i]] # 直接查询
                            if not country_name in countries:
                                countries.append(country_name)
                            break
                        else:
                            i += 1
            flink_element = selector.xpath(
                "//div[@class=\"icons portlet\"]//a/@href")
            if len(flink_element):
                for flink in flink_element:
                    flinks.append(flink)
            mh.add_new_content(pmid, title, authors, journal, ojournal, journal_if,
                               journal_zone, issue, abstract, key_words, institues, countries, flinks)
            msg.msg("record", pmid, "retrieved", "succ",
                    "info", msg.display, msg.stat)
            break
        except Exception, e:
            msg.msg("record", pmid, "retrieved",
                    "retried", "notice", msg.display)
            msg.msg("record", pmid, "retrieved", str(e), "error", msg.log)
            tries -= 1
            time.sleep(config.request_refresh_wait)  # 如果抓不成功，就先休息3秒钟

    else:
        msg.msg("record", pmid, "retrieved", "fail",
                "error", msg.display, msg.log)
        return 0  


def run_detail_crawler(project, sstr, record_number):
    pmid_list = get_pmid_list(project, sstr, record_number)
    pool = Pool(config.detail_crawler_number)  # 实例化进程池
    pool.map(crawl_detail, pmid_list)
    pool.close() # 关闭进程池
    pool.join() # 等待所有进程结束


if __name__ == '__main__':
    run_detail_crawler("lab on chip", "organ,on,chip", 10000)
