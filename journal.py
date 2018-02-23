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
"""

from __future__ import division  # python除法变来变去的，这句必须放开头
import sys
import re
import requests
from lxml import etree

import mongodb_handler as mh
import agents
import message as msg
import utilities as ut
import config


journal_name_list = mh.read_journal_name_all()  # 数据
ojournal_name_list = mh.read_ojournal_name_all()  # 读取


def journal_name_wash(journal_name_raw):  # 原始名称清洗（主要针对各种括号和标点、解释、注释）
    re_bracket = re.compile("[\\[\\(](.*?)[\\]\\)]")  # 去处括号解释
    re_explaination = re.compile(" ??[:=].*")  # 去处冒号后的解释
    journal_name = journal_name_raw.replace('&amp;', "&").replace(
        ',', '').replace(".", '')  # &是部分名称中包含的
    journal_name = re_bracket.sub('', journal_name)
    journal_name = re_explaination.sub('', journal_name)
    journal_name = journal_name.upper()  # 清洗过的名称全大写
    msg.msg("journal name", journal_name_raw, "washed",
            journal_name, "debug", msg.display)
    return journal_name


def get_official_name(journal_name_raw, proxy=None):  # 查找杂志的全名，支持模糊查询，只输出最符合的那个
    url = "http://www.letpub.com.cn/journalappAjax.php?querytype=autojournal&term=" + \
        journal_name_raw.replace("&", "%26").replace(" ", "+")
    tries = config.request_dp_tries
    while tries > 0:
        try:
            opener = requests.Session()
            doc = opener.get(url, timeout=20, headers=agents.get_header()).text
            list = doc.split('},{')  # 获取列表，但是只有最match的被采纳
            journal_name_start = list[0].find("label") + 8
            journal_name_end = list[0].find("\",\"", journal_name_start)
            journal_name = list[0][journal_name_start:journal_name_end]
            journal_name = journal_name.upper()  # 查找到的名字也是全大写
            msg.msg("journal name", journal_name_raw, "web retrieved",
                    journal_name, "debug", msg.display)
            return journal_name
            break
        except Exception, e:
            msg.msg("journal name", journal_name, "web retrieved",
                    "retried", "debug", msg.display)
            msg.msg("journal name", journal_name,
                    "web retrieved", str(e), "error", msg.log)
            tries -= 1
            time.sleep(config.request_refresh_wait)
    else:
        msg.msg("journal name", journal_name, "web retrieved",
                "fail", "error", msg.log, msg.display)
        return ""


def get_journal_info(ojournal_name, proxy=None):  # 查找杂志影响因子、分区, 要求输入精准
    url = "http://www.letpub.com.cn/index.php?page=journalapp&view=search"
    search_str = {
        "searchname": "",
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
    search_str["searchname"] = ojournal_name
    tries = config.request_dp_tries
    while tries > 0:
        try:
            opener = requests.Session()
            doc = opener.post(url, timeout=20, data=search_str).text
            selector = etree.HTML(doc.encode("utf-8"))
            journal_detail_element = selector.xpath(
                "//td[@style=\"border:1px #DDD solid; border-collapse:collapse; text-align:left; padding:8px 8px 8px 8px;\"]")
            if len(journal_detail_element):
                impact_factor = journal_detail_element[2].xpath('string(.)')
                publication_zone = journal_detail_element[3].xpath('string(.)')[
                    0]
            else:
                impact_factor = ""
                publication_zone = ""
            msg.msg("journal info", ojournal_name,
                    "web retrieved", "succ", "debug", msg.display)
            return impact_factor, publication_zone
            break
        except Exception, e:
            msg.msg("journal info", ojournal_name, "web retrieved",
                    "retried", "debug", msg.display)
            msg.msg("journal info", ojournal_name,
                    "web retrieved", str(e), "error", msg.log)
            tries -= 1
            time.sleep(config.request_refresh_wait)
    else:
        msg.msg("journal info", ojournal_name, "web retrieved",
                "fail", "error", msg.log, msg.display)
        return "", ""


# def journal_detail(journal_name, proxy=None):  # 使用使用的函数，自带储存功能
#     if journal_name in journal_name_list:  # 如果使用普通名称查询得到
#         record = mh.read_journal_detail(journal_name)  # 使用普通名称查询普通名称数据库
#         msg.msg("journal record", journal_name, "local retrieved",
#                 "succ", "debug", msg.log, msg.display)
#         return record
#     else:  # 如果使用普通名称查询不到，将普通名称通过网络转化为正式名称，再查询正式名称数据库
#         washed_journal_name = journal_name_wash(journal_name)  # 清洗文本，并大写
#         ojournal_name = get_official_name(
#             washed_journal_name)  # 清洗后的输入，输出官方精准名（全大写）
#         if ojournal_name in ojournal_name_list:  # 如果数据库中已经有了
#             record = mh.read_ojournal_detail(ojournal_name)  # 使用正式名称查询正式名称数据库
#             # 新生成一个记录，用新的普通名称
#             mh.add_journal(journal_name, record[1], record[2], record[3])
#             if not journal_name in journal_name_list:
#                 journal_name_list.append(journal_name)  # 新的普通名称加到集合
#             if not ojournal_name in ojournal_name_list:
#                 ojournal_name_list.append(ojournal_name)
#             msg.msg("journal record", ojournal_name, "local retrieved",
#                     "succ", "debug", msg.log, msg.display)
#             return record
#         else:  # 都还查不到
#             journal_info = get_journal_info(ojournal_name)  # 通过网络查询（新的杂志）
#             journal_if = journal_info[0]
#             journal_zone = journal_info[1]
#             if journal_if and journal_zone:  # 这两个数都存在才存
#                 mh.add_journal(journal_name, ojournal_name,
#                                journal_if, journal_zone)  # 注意只储存大写
#                 if not journal_name in journal_name_list:
#                     journal_name_list.append(journal_name)  # 新的普通名称加入集合
#                 if not ojournal_name in ojournal_name_list:
#                     ojournal_name_list.append(ojournal_name)  # 新的正式名称加入集合
#                 msg.msg("journal record", journal_name, "web retrieved",
#                         "succ", "debug", msg.log, msg.display)
#             data = journal_name, ojournal_name, journal_if, journal_zone
#             return data


def journal_detail(journal_name):
    record = mh.read_journal_detail(journal_name) # 直接试一下
    if record:
        msg.msg("journal record", journal_name, "local retrieved","succ", "debug", msg.display)
        return record
    else:
        wjournal_name = journal_name_wash(journal_name) # 清洗过的在正式名里试一下
        record = mh.read_ojournal_detail(wjournal_name)
        if record:
            msg.msg("journal record", journal_name, "local retrieved","succ", "debug", msg.display)
            return record
        else:
            ojournal_name  = get_official_name(wjournal_name) # 网络正式名在正式名里试一下
            record = mh.read_ojournal_detail(ojournal_name)
            if record:
                msg.msg("journal record", journal_name, "web retrieved","succ", "debug", msg.display)
                return record
            else:
                journal_info = get_journal_info(ojournal_name) # 网络正式名在网络查一下
                journal_if = journal_info[0]
                journal_zone = journal_info[1]
                mh.add_journal(journal_name, ojournal_name, journal_if, journal_zone) # 新杂志储存
                msg.msg("journal record", journal_name, "web retrieved","succ", "debug", msg.display)
                data = journal_name, ojournal_name, journal_if, journal_zone
                return data



if __name__ == '__main__':
    # print journal_detail("nature protocols:")
    print get_official_name("OBSTETRICS AND GYNECOLOGY")
