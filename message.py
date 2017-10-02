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

display_protocol = 9
log_protocol = 9

def log(task = "unscheduled",ctime, loginfo, logtype):
    if log_protocol == 9:
        mh.add_new_log(task, ctime, loginfo, logtype)
    elif log_protocol == 2 and logtype in ["important", "error", "notice", "sum"]:
        mh.add_new_log(task, ctime, loginfo, logtype)
    elif log_protocol == 1 and logtype == "important":
        mh.add_new_log(task, ctime, loginfo, logtype)
    else:
        pass

def display(ctime, msg, msgtype):
    if display_protocol == 9:
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 2 and msgtype in ["important", "error", "notice", "sum"]:
        screen.add_new_display(ctime, msg, msgtype)
    elif display_protocol == 1 and msgtype == "important":
        screen.add_new_display(ctime, msg, msgtype)
    else:
        pass

def stats(ctime, info, infotype):


