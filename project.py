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
   2018-08-31: 
-------------------------------------------------
"""
import sys
import os
import data_handler as dh
import utilities

reload(sys)  
sys.setdefaultencoding('utf8')

project_set = [] # 把project.csv里面的信息先预读到内存

def projects_read():
    projects = dh.csv_read("universal", "project")
    return projects

def project_name():
    project_names = []
    for project in project_set:
        project_name.append(project[0])
    return project_names

def project_key_words(project_name):
    key_words = []
    for project in project_set:
        if project[0] == project_name:
            key_words.append(project[1])
    return key_words

if __name__ == '__main__':
    print project_read()
    # print project_name()
