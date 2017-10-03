# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: message.py
   Description: 所有子程序运行信息导出
   Author: Dexter Chen
   Date：2017-09-19
-------------------------------------------------
   Development Note：
   1. 处理信息，决定是否log
   2. 根据显示模式，决定如何显示
   3. 把需要显示的传递给输出screen，web
-------------------------------------------------
   Change Log:
   2018-10-02: 
-------------------------------------------------
"""

import mongodb_handler as mh
import screen
import stats

display_protocol = 9
log_protocol = 9

def log(task, ctime, loginfo, logtype): # 用于日志的信息
    if log_protocol == 9:
        mh.add_new_log(task, ctime, loginfo, logtype)
    elif log_protocol == 2 and logtype in ["important", "error", "notice", "sum"]:
        mh.add_new_log(task, ctime, loginfo, logtype)
    elif log_protocol == 1 and logtype == "important":
        mh.add_new_log(task, ctime, loginfo, logtype)
    else:
        pass

def display(ctime, msg, msgtype): # 用于显示的信息
    if display_protocol == 9:
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 2 and msgtype in ["important", "error", "notice", "sum"]:
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 1 and msgtype == "important":
        screen.add_new_display(ctime, msg, msgtype)
    else:
        pass

def stat(stats_info, stats_infotype): # 用于统计的信息
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
