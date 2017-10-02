# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: text_clean.py
   Description: 在抓取过程中即时清洗文字
   Author: Dexter Chen
   Date：2017-10-01
-------------------------------------------------
   Development Note：
   1. 
-------------------------------------------------
"""

import re
import dictionary

# 用于根据字典文件替换
def word_replace(data):
    for (k,j) in dictionary.replace_dict.items():
        data = data.replace(k,j)
    return data


# 用正则表达式进行，正则表达式可以不断加
def regexp_replace(data):
    # 用正则表达式去除标签
    re_html = re.compile("</?\w+[^>]*>\s?") # 清除所有html标签
    re_label = re.compile("label=\"\"[\w\s]*?\"\">?\s?") # 清除非html标签
    re_nlmcatagory = re.compile("nlmcategory=\"\"[\s\w]+\"\">?\s?") # 清除nlm标签
    data = re_html.sub('',data)
    data = re_label.sub('',data)
    data = re_nlmcatagory.sub('',data)
    return data

def text_clean(data):
    data = regexp_replace(data)
    data = word_replace(data)
    return data
    

if __name__ == '__main__':
    pass
