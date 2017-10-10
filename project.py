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
   1. 扫描所有项目文件夹，项目文件夹数可大于csv中登记数
   2. 根据需要新建项目，生成必要文件（提醒重复）；删除只需在csv中删除(保留文件夹)
   3. 
-------------------------------------------------
   Change Log:
   2018-08-31: 
-------------------------------------------------
   格式：
   project: 名称，描述，创建时间
   key_words（可以是表达式）
   log: 信息，信息类型，生成时间
-------------------------------------------------
"""
import sys
import os
import utilities as ut
import mongodb_handler as mh

reload(sys)
sys.setdefaultencoding('utf8')

projects = [] # 把project.csv里面的信息先预读到内存
key_words = [] # 关键词 

def projects_read():
    projects = mh.
    project_set = dh.csv_read("universal", "project")
    projects = map(lambda x: x.split(",|,"), project_set)

def key_words_read(project_name):
    global key_words
    key_words_set = dh.text_read(project_name,"key_words")
    key_words = key_words_set.split("\n")

def project_add(project_name, project_description):
    if not dh.check_folders(project_name, "folder"): # 如果没有对应文件夹
        dh.new_project_files(project_name) # 新建文件
        project_set = dh.text_read("universal","project").split("\n")
        time.sleep(0.1) # 确保文件夹读取后关闭
        new_project = project_name, project_description, ut.time_str("full")
        project_set.append(new_project)
        dh.text_write(project_set,"universal","project","w")
    else:
        op.output("Folder already exist", "warning", ut.time_str("full"))


def project_des_update(project_name, project_description): 
    i = 0
    for i in len(project_set):
        if project_set[i].split(",|,")[0] == project_name:

            op.output("Project description updated",
                      "notice", ut.time_str("full"))
    else:
        op.output('No project found', "notice", ut.time_str("full"))


def project_delete(project_name):
    for project in project_set:
        if project[0] == project_name:
            del project
            dh.csv_write(project_set, "universal", "project", "wb")
            op.output("Project deleted", "notice", ut.time_str("full"))
    else:
        op.output('No project found', "notice", ut.time_str("full"))


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
    project_add("dexter", "test project for Dexter")