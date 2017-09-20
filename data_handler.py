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
   2. 根据文件类型，提取完整路径
   3. 读取、写入数据
-------------------------------------------------
   Change Log:
   2017-09-14: 复活，把operator改为handler 
   2017-09-16: 所有数据目录更改为data文件夹内
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
    path_dict = {
        "project": "_project.txt", 
        "journal": "_journal.csv", 
        "history": "_history.txt",
        "key_words":"_key_words.txt", 
        "log":"_log.txt",
        "stats":"stats.txt", # 统计文件
        "data": "_data.csv", 
        "data_temp": "_data_temp.csv", 
        "data_tab_txt": "_data_tab_txt.txt"
    }
    path = cur_file_dir() + "/data/" + project_name + "/"
    try:
        file_dir = path + project_name + path_dict.get(file_type)
        return file_dir
    except Expression as identifier:
        return u" Error: Wrong file type"

# 通用读取
def csv_read(project_name, file_type):
    data_set = []
    with open(file_name(project_name, file_type), 'rb+') as csvfile:
        data = csv.reader(csvfile, dialect='excel')
        for row in data:
            data_set.append(','.join(row))
    return data_set

def csv_write(data, project_name, file_type, write_way = "ab+"): # 默认是追加，可以用参数强制覆写
    with open(file_name(project_name, file_type), write_way) as csvfile:
        data_writer = csv.writer(csvfile, dialect='excel')
        data_writer.writerow(zip(data))

def text_read(project_name, file_type):
    with open(file_name(project_name, file_type), 'rb') as f:
        text = f.read()
    return text

def text_write(data, project_name, file_type, write_way = "ab+"): # 默认是追加，可以用参数强制覆写
    with open(file_name(project_name, file_type), write_way) as f:
        f.write(data + ',')

def check_folders(project_name, file_type): # 检查某个文件夹是否在，不在回复False，在回复True
    if file_type == "folder": # 检查文件夹在不在
        path = path = cur_file_dir() + "/data/" + project_name + "/"
    else: # 检测具体文件在不在
        path = cur_file_dir() + "/data/" + project_name + "/" + project_name + file_name(project_name, file_type)
    b = os.path.isdir(path)
    return b

def new_project_files(project_name):  # 生成文件夹以及原始文件：数据、历史、关键词
    path = cur_file_dir() + "/data/" + project_name + "/"
    os.mkdir(path)  # 根据path生成文件夹，下面生成所有项目所需文件
    new_data_file = open(file_name(project_name, "data"), "w")
    new_hisotry_file = open(file_name(project_name, "history"), 'w')
    new_key_words_file = open(file_name(project_name, "key_words"), "w")
    new_data_file.close()
    new_hisotry_file.close()
    new_key_words_file.close()

if __name__ == '__main__':
    a = text_read("cancer","key_words").split('\n')
    a.append("hello,world")
    text_write(a,"cancer","key_words")
