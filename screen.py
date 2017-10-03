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
   1.接收信息，根据信息种类，选择打印颜色与存留时间
-------------------------------------------------
   Change Log:
   2017-09-14：重新复活。输出不涉及md，html和web
-------------------------------------------------
   Message 属性：
   颜色样式 + 显示时间（1，3，5） + 优先级（0-4越小越重要）
-------------------------------------------------
"""
import sys
import os
from colorama import init, Fore, Back, Style
import utilities as ut

reload(sys)
sys.setdefaultencoding('utf8')

init(autoreset=True)

info_type_def = {
    "info": (Back.GREEN + Fore.WHITE, 3, 3),
    "warning": (Back.YELLOW + Fore.WHITE, 10, 1),
    "error": (Back.RED + Fore.WHITE, 10, 1),
    "notice":(Back.LIGHTCYAN_EX + Fore.BLACK, 5, 2),
    "time_stamp": (Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX, 5, 4)
}

message_set = []

def add_new_display(ctime, info, info_type):
    print(info_type_def["time_stamp"] + "[" + ctime + "]"),
    print(info_type_def[info_type][0] + "[" + info_type + "]"),
    print info

class Message:
    def __init__(info, info_type, ctime):
        self.info = info
        self.info_type = info_type
        self.ctime = ctime
        self.end_time = ut.time_str("full",info_type_def[self.info_type][1]/3600)
        self.is_logged = 0

    def display():
        print(info_type_def["time_stamp"] + "[" + self.ctime + "]"),
        print(info_type_def[self.info_type][0] + "[" + self.info_type + "]"),
        print info

    def log_error():
        if self.info_type == "error":
            rl.run_log(self.info, self.info_type, self.ctime)
            self.is_logged = 1

    def update():
        if not self.is_logged:
            self.log_error()
        if ut.time_str < self.end_time:
            self.display()
        else:
            #delete self from list
            pass



if __name__ == '__main__':
    output("dexter is here", "info", "1991-12-13 03:45:23")
