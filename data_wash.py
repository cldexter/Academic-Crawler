# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: data_wash.py
   Description: 数据清洗、变换，不涉及存储（交给operate）
   Author: Dexter Chen
   Date：2017-09-01
-------------------------------------------------
   Development Note：
   1. 通过正则表达式清洗
   2. 通过替换清洗
   3. 
-------------------------------------------------
   Change Log:
   2018-09-14: 重新复活
-------------------------------------------------
"""
from __future__ import division # python除法变来变去的，这句必须放开头
import sys
import os
import re
import data_operate
import dictionary

reload(sys)
sys.setdefaultencoding('utf8')

# 用于根据字典文件替换
def word_replace(data):
    for (k,j) in dictionary.replace_dict.items():
        data = data.replace(k,j)
    return data

# 把用“|”隔开的str还原为list（原始状态）可选：1.',|,' 2.'	'
def data_2_list(data,dilimiter):
    data_list = data.split(dilimiter)
    return data_list

# 用正则表达式进行，正则表达式可以不断加
def regexp_replace(data):
    # 用正则表达式去除标签
    re_html = re.compile("</?\w+[^>]*>\s?")
    re_label = re.compile("label=\"\"[\w\s]*?\"\">?\s?")
    re_nlmcatagory = re.compile("nlmcategory=\"\"[\s\w]+\"\">?\s?")
    data = re_html.sub('',data)
    data = re_label.sub('',data)
    data = re_nlmcatagory.sub('',data)
    return data

# 把list改为可以再次储存的格式，并储存
def list_restore(list,project_name):
    record_str = list[0],"|",list[1],"|",list[2],"|",list[3],"|",list[4],"|",list[5],"|",list[6],"|",list[7],"|",list[8],"|",list[9],"|",list[10]
    data_operate.data_write(record_str,project_name,"data_temp")

# 清洗文字的主程序
def text_wash(project_name):
    data_set = data_operate.data_read(project_name,"data_tab_txt")
    for data_item in data_set:
        try:
            data_item = word_replace(data_item)
            data_item = regexp_replace(data_item)
            data_list = data_2_list(data_item,'	')
            list_restore(data_list,project_name)
            i += 1
        except Exception, e:
            print e

if __name__ == '__main__':
    text_wash("cancer")
