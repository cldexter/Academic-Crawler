# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: message.py
   Description: 对外输出的log，显示及统计信息处理
   Author: Dexter Chen
   Date：2017-09-19
-------------------------------------------------

"""

import mongodb_handler as mh
import screen
import stats
import utilities as ut
import config


def msg(who, identifier, action, result, info_type, *args):
    '''*args可以为log, display, stat一个或多个'''
    for fn in args:
        fn(ut.time_str("full"), who, identifier, action, result, info_type)


def log(when, who, identifier, action, result, info_type):  # 用于日志的信息
    if config.log_protocol == 9:
        mh.add_new_log(when, who, identifier, action, result, info_type)
    elif config.log_protocol == 5 and info_type in ["important", "error", "notice", "debug", "info"]:
        mh.add_new_log(when, who, identifier, action, result, info_type)
    elif config.log_protocol == 4 and info_type in ["important", "error", "notice", "info"]:
        mh.add_new_log(when, who, identifier, action, result, info_type)
    elif config.log_protocol == 3 and info_type in ["important", "error", "notice"]:
        mh.add_new_log(when, who, identifier, action, result, info_type)
    elif config.log_protocol == 2 and info_type in ["important", "error"]:
        mh.add_new_log(when, who, identifier, action, result, info_type)
    elif config.log_protocol == 1 and info_type == "important":
        mh.add_new_log(when, who, identifier, action, result, info_type)
    else:
        pass


def display(when, who, identifier, action, result, info_type):  # 用于显示的信息
    if config.display_protocol == 9:
        screen.add_new_display(when, who, identifier,
                               action, result, info_type)
    elif config.display_protocol == 5 and info_type in ["important", "error", "notice", "debug", "info"]:
        screen.add_new_display(when, who, identifier,
                               action, result, info_type)
    elif config.display_protocol == 4 and info_type in ["important", "error", "notice", "info"]:
        screen.add_new_display(when, who, identifier,
                               action, result, info_type)
    elif config.display_protocol == 3 and info_type in ["important", "error", "notice"]:
        screen.add_new_display(when, who, identifier,
                               action, result, info_type)
    # 只记录错误
    elif config.display_protocol == 2 and info_type in ["important", "error"]:
        screen.add_new_display(when, who, identifier,
                               action, result, info_type)
    elif config.display_protocol == 1 and info_type == "important":
        screen.add_new_display(when, who, identifier,
                               action, result, info_type)
    else:
        pass


def stat(when, who, identifier, action, result, info_type):  # 用于统计的信息
    if result == "succ":
        if who == "sum page":
            stats.success_sum_page += 1
        elif who == "record":
            stats.success_record += 1
        elif who == "pmid":
            stats.success_pmid += 1
            stats.c_skipped_pmid = 0
        elif who == "crawl pmid":
            if result == "started":
                stats.crawl_pmid_start = ut.time_str("full")
            elif result == "finished":
                stats.crawl_pmid_finish = ut.time_str("full")
        elif who == "crawl detail":
            if result == "started":
                stats.crawl_detail_start = ut.time_str("full")
            if result == "finished":
                stats.crawl_detail_finish = ut.time_str("full")
    elif result == "fail":
        if who == "sum page":
            stats.failed_sum_page += 1
        elif who == "record":
            stats.failed_record += 1
        elif who == "pmid":
            stats.failed_pmid += 1
    elif result == "proc":
        if who == "sum page":
            stats.processed_sum_page += 1
        elif who == "record":
            stats.processed_record += 1
        elif who == "pmid":
            stats.processed_pmid += 1
    elif result == "skip":
        if who == "sum page":
            stats.skipped_sum_page += 1
        elif who == "record":
            stats.skipped_record += 1
        elif who == "pmid":
            stats.skipped_pmid += 1
            stats.c_skipped_pmid += 1


if __name__ == '__main__':
    msg("sp", '4', 'loaded in phantomjs', 'info', log, display)
