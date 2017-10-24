# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: screen.py
   Description: 在屏幕上打印的处理
   Author: Dexter Chen
   Date：2017-09-01
-------------------------------------------------
   Development Note：
   1.最上方显示统计数据，状态数据
   2.接收信息，根据信息种类，选择打印颜色与存留时间
-------------------------------------------------

"""
import sys
import os
from colorama import init, Fore, Back, Style
import utilities as ut

reload(sys)
sys.setdefaultencoding('utf8')

init(autoreset=True)

color_code = {
    "info":(Back.GREEN + Fore.BLACK),
    "important":(Back.BLACK + Fore.WHITE),
    "error":(Back.RED + Fore.LIGHTWHITE_EX),
    "notice":(Back.YELLOW + Fore.BLACK),
    "debug":(Back.LIGHTCYAN_EX + Fore.BLACK),
    "time_stamp":(Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX)
}

message_set = []

def add_new_display(when, who, identifier, action, result, info_type):
    print(color_code["time_stamp"] + " [" + when + "] "),
    print(color_code[info_type] + " [" + info_type + "] "),
    print who, identifier, action, result


def time_box():# 把时间相关的列出来
    print " ---------------------------------------------------------------"
    print " │     Current Time    │      Start Time     │   Elapsed Time  │"
    print " │ " + ut.time_str("full") + " │ " + ut.time_str("full") + " │ " + "  ?? Hr ?? min " + " │"
    print " ---------------------------------------------------------------"

def project_menu():
    pass
    

if __name__ == '__main__':
    add_new_display("10:10:10", "dexter", "121131311", "is here", "succ", "debug")
    add_new_display("10:10:10", "dexter", "121131311", "is here", "succ", "notice")
    add_new_display("10:10:10", "dexter", "121131311", "is here", "succ", "info")
    add_new_display("10:10:10", "dexter", "121131311", "is here", "succ", "important")
    add_new_display("10:10:10", "dexter", "121131311", "is here", "succ", "error")
