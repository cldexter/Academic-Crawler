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
import utilities as ut
import output as op

reload(sys)  
sys.setdefaultencoding('utf8')

projects = [] # 把project.csv里面的信息先预读到内存

def projects_read():
    project_set = dh.csv_read("universal", "project")
    projects = map(lambda x:x.split(",|,"),project_set)
    return projects

def project_add(project_name):
    if not dh.check_folders(project_name, "folder"):
        dh.new_project_files(project_name)
    else:
        op.output("Folder already exist","warning",ut.time_str("full"))

def project_des_update(project_name, project_description):
    i = 0
    for i in len(project_set):
        if project_set[i].split(",|,")[0] == project_name:

            op.output("Project description updated","notice",ut.time_str("full"))
    else:
        op.output('No project found',"notice",ut.time_str("full"))

def project_delete(project_name):
    for project in project_set:
        if project[0] == project_name:
            del project
            dh.csv_write(project_set, "universal", "project", "wb")
            op.output("Project deleted","notice",ut.time_str("full"))
    else:
        op.output('No project found',"notice",ut.time_str("full"))


def project_name():
    project_names = []
    for project in project_set:
        project_names.append(project[0])
    return project_names

def project_key_words(project_name):
    key_words = []
    for project in project_set:
        if project[0] == project_name:
            key_words.append(project[1])
    return key_words

if __name__ == '__main__':
    print projects_read()P