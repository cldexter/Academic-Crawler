# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: utilities.py
   Description: 多次用到的小工具：时间，文字清理等
   Author: Dexter Chen
   Date：2017-09-14
-------------------------------------------------
   Development Note：
   1. 时间戳：统一用日期 + 时间的形式
   2. 显示：屏幕只显示时间，不现实日期
-------------------------------------------------
   Change Log:
   2017-09-14: 复活，把operator改为handler
   2017-09-17: 更新时间工具，可以计算后续多少小时
-------------------------------------------------
"""
import sys
import re
import dictionary
import datetime
import thread
from threading import Timer

# 输出时间，带日期和不带; delta_hr 是往后数多少小时，负数往前数


def time_str(type="full", delta_hr=0):
    if type == "full":  # 完整时间
        time_format = '%Y-%m-%d %X'
    if type == "time":  # 只有时间
        time_format = "%X"
    time_str = datetime.datetime.now()
    time = time_str + datetime.timedelta(hours=delta_hr)
    return time.strftime(time_format)


# 用于根据字典文件替换
re_dict = dictionary.replace_dict


def dict_replace(data, re_dict):
    for (k, j) in re_dict.items():
        data = data.replace(k, j)
    return data


# 用正则表达式进行，正则表达式可以不断加
re_html = "</?\w+[^>]*>\s?"  # 清除所有html标签
re_label = "label=\"\"[\w\s]*?\"\">?\s?"  # 清除非html标签
re_nlmcatagory = "nlmcategory=\"\"[\s\w]+\"\">?\s?"  # 清除nlm标签


def regexp_replace(data, re_data):
    # 用正则表达式去除标签
    re_content = re.compile(re_data)  # 清除所有html标签
    data = re_content.sub('', data)
    return data


def cur_file_dir():  # 获取脚本路径
    path = sys.path[0]
    return path


class Watchdog:  # 看门狗程序，防止运行卡死
    def __init__(self):
        ''' Class constructor. The "time" argument has the units of seconds. '''
        self._time = maxPorcessTime
        return

    def StartWatchdog(self):
        ''' Starts the watchdog timer. '''
        self._timer = Timer(self._time, self._WatchdogEvent)
        self._timer.daemon = True
        self._timer.start()
        return

    def PetWatchdog(self):
        ''' Reset watchdog timer. '''
        self.StopWatchdog()
        self.StartWatchdog()
        return

    def _WatchdogEvent(self):
        cPrint(u'\n ●调 等待太久，程序强制跳过 \n', COLOR.RED)
        self.StopWatchdog()
        thread.interrupt_main()
        return

    def StopWatchdog(self):
        ''' Stops the watchdog timer. '''
        self._timer.cancel()


if __name__ == '__main__':
    print time_str("full")
