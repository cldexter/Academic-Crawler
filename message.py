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

info_code = {
    "101":"retrieved record successfully"
}


def msg(info, info_type, *args): #*args 表明要执行的程序，可以是一个或者多个：log，display，stat
    for function in *args:
        function(ut.time_str("full"), info, info_type)

    
def log(ctime, loginfo, logtype): # 用于日志的信息
    if log_protocol == 9:
        mh.add_new_log(ctime, loginfo, logtype)
    elif log_protocol == 5 and logtype in ["important", "error", "notice", "debug", "info"]:
        mh.add_new_log(ctime, loginfo, logtype)
    elif log_protocol == 4 and logtype in ["important", "error", "notice", "info"]:
        mh.add_new_log(ctime, loginfo, logtype)
    elif log_protocol == 3 and logtype in ["important", "error", "notice"]:
        mh.add_new_log(ctime, loginfo, logtype)
    elif log_protocol == 2 and logtype in ["important", "error"]:
        mh.add_new_log(ctime, loginfo, logtype)
    elif log_protocol == 1 and logtype == "important":
        mh.add_new_log(ctime, loginfo, logtype)
    else:
        pass

def display(ctime, msg, msgtype): # 用于显示的信息
    if display_protocol == 9:
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 5 and msgtype in ["important", "error", "notice", "debug", "info"]: 
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 4 and msgtype in ["important", "error", "notice", "info"]: 
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 3 and msgtype in ["important", "error", "notice"]: 
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 2 and msgtype in ["important", "error"]: # 只记录错误
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 1 and msgtype == "important":
        screen.add_new_display(ctime, msg, msgtype)
    else:
        pass

def stat(ctime, stats_info, stats_infotype): # 用于统计的信息
    if stats_infotype ==  "succ":
        if stats_info == "sum_page":
            stats.success_sum_page += 1
        elif stats_info == "record":
            stats.success_record += 1
    elif stats_infotype == "fail":
        if stats_info == "sum_page":
            stats.failed_sum_page += 1
        elif stats_info == "record":
            stats.failed_record += 1
    elif stats_infotype == "proc":
        if stats_info == "sum_page":
            stats.processed_sum_page += 1
        elif stats_info == "record":
            stats.processed_record += 1
    elif stats_infotype == "skip":
        if stats_info == "sum_page":
            stats.skipped_sum_page += 1
        elif stats_info == "record":
            stats.skipped_record += 1

if __name__ == '__main__':
    pass
