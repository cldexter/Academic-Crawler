# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: data_operate.py
   Description: 所有数据读取的操作，不涉及数据变换
   Author: Dexter Chen
   Date：2017-09-09
-------------------------------------------------
   Development Note：
   1. 判断文件路径
   2. 判断文件类型
-------------------------------------------------
   Change Log:
   2018-09-09: 
-------------------------------------------------
"""
from __future__ import division # python除法变来变去的，这句必须放开头
import sys
import os
import csv
import time

reload(sys)
sys.setdefaultencoding('utf8')

def cur_file_dir():#获取脚本路径
    path = sys.path[0]
    return path

def file_name(project_name,file_type):#用于查询当前的文件位置和名称
    path = cur_file_dir() + "/" + project_name +"/" 
    if file_type == "history":
        return path+project_name+"_history.txt"
    if file_type == "data":
        return path+project_name+"_data.csv"
    if file_type == "data_temp":
        return path+project_name+"_data_temp.csv"
    if file_type == "data_tab_txt":
        return path+project_name+"_data_tab_txt.txt"
    if file_type == "key_words":
        return path+project_name+"_key_words.csv"
    else:
        return u" ○ Error: Wrong file type"
# 通用读取
def data_read(project_name,file_type):#所有读取都用这个
    data_set = []
    with open(file_name(project_name,file_type), 'rb') as csvfile:
        data = csv.reader(csvfile, dialect='excel')
        for row in data:
            data_set.append(','.join(row))
    return data_set

def data_write(data,project_name,file_type):#所有储存都这样弄
    with open(file_name(project_name,file_type), 'ab+') as csvfile:
        data_writer = csv.writer(csvfile, dialect='excel')
        data_writer.writerow(data)

def text_read(project_name,file_type):#读取pmid库，自动关闭文件
    with open(file_name(project_name,file_type),'rb') as f:
        pmid_set = f.read()
    return pmid_set

def text_write(data,project_name,file_type):#存入pmid,自动关闭文件
    with open(file_name(project_name,file_type),"ab+") as f:
        f.write(data +',')
