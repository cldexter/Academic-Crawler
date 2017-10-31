# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: utilities.py
   Description: 多次用到的小工具：时间，文字清理等
   Author: Dexter Chen
   Date：2017-09-14
-------------------------------------------------
"""
import sys
import time
import re
import dictionary
import datetime
import thread
from threading import Timer

# 输出时间，带日期和不带; delta_hr 是往后数多少小时，负数往前数


def time_str(type="full", delta_min=0): # 自然时间的时间戳
    if type == "full":  # 完整时间
        time_format = '%Y-%m-%d %X'
    if type == "time":  # 只有时间
        time_format = "%X"
    time_str = datetime.datetime.now()
    time = time_str + datetime.timedelta(minutes=delta_min)
    return time.strftime(time_format)


def time_object(time_str):
    return time.strptime(time_str, "%Y-%m-%d %X")


def str_duration(early_time_str, late_time_str): # 计算两个时间str之间的时间差，默认输出h，也可输出min
    early_time_object = datetime.datetime.strptime(early_time_str, "%Y-%m-%d %X")
    late_time_object = datetime.datetime.strptime(late_time_str, "%Y-%m-%d %X")
    duration_delta = late_time_object - early_time_object
    duration_in_seconds = int(duration_delta.total_seconds())
    return duration_in_seconds

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
re_email_pm = "Electronic address:.*"
re_email_general = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


def regexp_replace(data, re_data):
    # 用正则表达式去除标签
    re_content = re.compile(re_data)  # 清除所有html标签
    data = re_content.sub('', data)
    return data


def cur_file_dir():  # 获取脚本路径
    path = sys.path[0]
    return path


if __name__ == '__main__':
    print str_duration("2010-10-10 10:10:10", "2010-10-10 11:10:10")
    print time_str("full")
    print time_str("full", 30)