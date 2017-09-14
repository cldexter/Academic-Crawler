# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: project.py
   Description: 处理与项目（增减改）相关的工作
   Author: Dexter Chen
   Date：2017-09-04
-------------------------------------------------
   Development Note：
   1.扫描所有项目，找到
-------------------------------------------------
   Change Log:
   2018-08-31: 建立输出方法：获取json，正确输出到屏幕 
-------------------------------------------------
"""
import sys
import os
import csv
import re
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
    else:
        return u" ○ Error: Wrong file type"

def text_read(project_name,file_type):#读取pmid库，自动关闭文件
    with open(file_name(project_name,file_type),'r') as f:
        pmid_set = f.read()
    return pmid_set

def text_write(data,project_name,file_type):#存入pmid,自动关闭文件
    with open(file_name(project_name,file_type),"wb") as f:
        f.write(data +',')
    time.sleep(0.1)

def projects_read():
    projects_set = []
    path = cur_file_dir() + "/" + "projects.csv"
    with open(path,"rU") as f:
        data = csv.reader(f,dialect="excel")
        for row in data:
            projects_set.append(','.join(row))

def project_write(data):#所有储存都这样弄
	with open(file_name(project_name,file_type), 'a') as csvfile:
	    data_writer = csv.writer(csvfile, dialect='excel')
	    data_writer.writerow(data)
	time.sleep(0.1)

def project_name():
    project_name = []
    for project in project_read():
        project_name.append(project_read().get["name"])
    return project_name

def project_key_words(project_name):
    project = project_read["name":project_name]
    project_key_words = project["keywords"]

def check_folders(project_name):#检查项目文件夹是否存在，项目文件夹一定包含了项目所需文件
    path = cur_file_dir() + "/" + project_name +"/"
    b = os.path.isdir(path)
    return b

def generate_files(project_name):#生成文件夹以及原始文件：数据、历史、关键词
    path = cur_file_dir() + "/" + project_name +"/" 
    os.mkdir(path)#根据path生成文件夹，下面生成所有项目所需文件
    new_data_file = open(path+project_name+"_data.csv",'w')
    new_hisotry_file = open(path+project_name+"_history.txt",'w')
    new_data_file.close()
    new_hisotry_file.close()

if __name__ == '__main__':
    print project_read()
    # print project_name()