# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: data_handler.py
   Description: 所有数据读取的操作，不涉及数据变换
   Author: Dexter Chen
   Date：2017-09-09
-------------------------------------------------
   Development Note：
   1. 判断文件路径
   2. 判断文件类型
-------------------------------------------------
   Change Log:
   2018-09-14: 复活，把operator改为handler 
-------------------------------------------------
"""
from __future__ import division  # python除法变来变去的，这句必须放开头
import sys
import os
import csv
import time

reload(sys)
sys.setdefaultencoding('utf8')

def cur_file_dir():  # 获取脚本路径
    path = sys.path[0]
    return path

def file_name(project_name, file_type):  # 用于查询当前的文件位置和名称
    path_dict = {"history": "_history.txt", "data": "_data.csv", "data_temp": "_data_temp.csv", "data_tab_txt": "_data_tab_txt.txt"
                 }
    path = cur_file_dir() + "/" + project_name + "/"
    try:
        file_dir = path + project_name + path_dict.get(file_type)
        return file_dir
    except expression as identifier:
        return return u" Error: Wrong file type"

# 通用读取
def csv_read(project_name, file_type):
    data_set = []
    with open(file_name(project_name, file_type), 'rb') as csvfile:
        data = csv.reader(csvfile, dialect='excel')
        for row in data:
            data_set.append(','.join(row))
    return data_set

def csv_write(data, project_name, file_type):
    with open(file_name(project_name, file_type), 'ab+') as csvfile:
        data_writer = csv.writer(csvfile, dialect='excel')
        data_writer.writerow(data)

def text_read(project_name, file_type):
    with open(file_name(project_name, file_type), 'rb') as f:
        text = f.read()
    return text

def text_write(data, project_name, file_type):
    with open(file_name(project_name, file_type), "ab+") as f:
        f.write(data + ',')
