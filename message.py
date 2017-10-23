# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: message.py
   Description: 对外输出的log，显示及统计信息处理
   Author: Dexter Chen
   Date：2017-09-19
-------------------------------------------------
   Development Note：
   1. 处理信息，决定是否log
   2. 根据显示模式，决定如何显示
   3. 把需要显示的传递给输出screen，web
-------------------------------------------------

"""

import mongodb_handler as mh
import screen
import stats
import utilities as ut

display_protocol = 9 # 定义哪种显示方法
log_protocol = 9 # 定义哪种记录方法

def msg(who, identifier, what, info_type, *args):
    '''*args可以为log, display, stat一个或多个'''
    for fn in args:
        fn(ut.time_str("full"), who, identifier, what, info_type)

    
def log(when, who, identifier, what, info_type): # 用于日志的信息
    if log_protocol == 9:
        mh.add_new_log(when, who, identifier, what, info_type)
    elif log_protocol == 5 and info_type in ["important", "error", "notice", "debug", "info"]:
        mh.add_new_log(when, who, identifier, what, info_type)
    elif log_protocol == 4 and info_type in ["important", "error", "notice", "info"]:
        mh.add_new_log(when, who, identifier, what, info_type)
    elif log_protocol == 3 and info_type in ["important", "error", "notice"]:
        mh.add_new_log(when, who, identifier, what, info_type)
    elif log_protocol == 2 and info_type in ["important", "error"]:
        mh.add_new_log(when, who, identifier, what, info_type)
    elif log_protocol == 1 and info_type == "important":
        mh.add_new_log(when, who, identifier, what, info_type)
    else:
        pass

def display(when, who, identifier, what, info_type): # 用于显示的信息
    if display_protocol == 9:
        screen.add_new_display(when, who, identifier, what, info_type)
    elif display_protocol == 5 and info_type in ["important", "error", "notice", "debug", "info"]: 
        screen.add_new_display(when, who, identifier, what, info_type)
    elif display_protocol == 4 and info_type in ["important", "error", "notice", "info"]: 
        screen.add_new_display(when, who, identifier, what, info_type)
    elif display_protocol == 3 and info_type in ["important", "error", "notice"]: 
        screen.add_new_display(when, who, identifier, what, info_type)
    elif display_protocol == 2 and info_type in ["important", "error"]: # 只记录错误
        screen.add_new_display(when, who, identifier, what, info_type)
    elif display_protocol == 1 and info_type == "important":
        screen.add_new_display(when, who, identifier, what, info_type)
    else:
        pass

def stat(who, info_type): # 用于统计的信息
    if info_type ==  "succ":
        if who == "sum_page":
            stats.success_sum_page += 1
        elif who == "record":
            stats.success_record += 1
    elif info_type == "fail":
        if who == "sum_page":
            stats.failed_sum_page += 1
        elif who == "record":
            stats.failed_record += 1
    elif info_type == "proc":
        if who == "sum_page":
            stats.processed_sum_page += 1
        elif who == "record":
            stats.processed_record += 1
    elif info_type == "skip":
        if who == "sum_page":
            stats.skipped_sum_page += 1
        elif who == "record":
            stats.skipped_record += 1

if __name__ == '__main__':
    msg("sp", '4', 'loaded in phantomjs', 'info', log, display)
