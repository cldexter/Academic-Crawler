# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: mongodb_handler.py
   Description: 处理一切与mongodb对接的工作
   Author: Dexter Chen
   Date：2017-09-28
-------------------------------------------------
   Development Note：
   1.为了减少其它函数复杂性，所有BSON构成在这里进行
-------------------------------------------------
   Change Log:

-------------------------------------------------
   格式：数据库名称
   论文内容在["papers"]["count"]（不分项目）
   项目在["papers"]["project"]
   任务在["papers"]["task"]
   运行日志在["papers"]["log"]
-------------------------------------------------
"""

from pymongo import *

my_record = {"pmid": "200000", "name": "dexter", "hello": "world"}

client = MongoClient('mongodb://localhost:27017/')  # 固定的不要变动


def get_db(data_type):  # 获取各个集合路径
    if data_type == "content":
        database = client["papers"]["content"]
    elif data_type == "project":
        database = client["papers"]["project"]
    elif data_type == "log":
        database = client["papers"]["log"]
    elif data_type == "task":
        database = client["papers"]["task"]
    elif data_type == "journal":
        database = client["papers"]["journal"]
    else:
        database = "error"
    return database


# 通用操作部分
def count_record(data_type):
    number = get_db(data_type).count()
    return number


def read_record_all(data_type):  # 获取某集合所有数据
    records = []
    if count_record(data_type) > 0:
        for record in get_db(data_type).find():
            records.append(record)
    return records


def add_record(data, data_type):
    get_db(data_type).insert_one(data)


# 对杂志的操作
def read_journal_name_all():
    journals = []
    for record in get_db("journal").find():
        journals.append(record['journal'])
    return journals


def read_journal_detail(journal_name):
    record = get_db("journal").find_one({"journal":journal_name})
    if record:
        data = record['journal'], record['if'], record['jzone']
    return data

def add_journal(journal_name, impact_factor, journal_zone):
    data = {"journal":journal_name, "if":impact_factor, "jzone":journal_zone}
    get_db("journal").insert_one(data)


# 对论文指定操作部分
def read_pmid_all():
    pmids = []
    for record in get_db("content").find():
        pmids.append(record['pmid'])
    return pmids


def add_new_content(project, sstr, ctime, source, pmid, title, author, journal, ojournal, impact_factor, jzone, issue, abstract, keyword, institue, flink): # 新增一个论文记录
    data = {"project": project, "sstr": sstr, "ctime": ctime, "status": 1, "source": source, "pmid": pmid, "title": title, "author": author, "journal": journal, "ojournal":ojournal, "if": impact_factor, "jzone": jzone,"issue": issue, "abstract": abstract, "keyword": keyword, "institue": institue, "irank": "", "country": "", "flink": flink, "usability": "", "relativeness": "", "quality": "", "highlight": "", "comment": ""}
    get_db("content").insert_one(data)


def update_content(pmid, new_content):  # 更新论文数据模块，注意new_content不需要双引号
    get_db("content").update_one({'pmid': pmid}, {"$set": new_content})


def del_content(pmid):
    get_db("content").delete_one({'pmid': pmid})


# 对log做制定操作
def add_new_log(task, ctime, loginfo, logtype):
    data = {"task":task, "ctime":ctime, "loginfo":loginfo, "logtype":logtype}
    get_db('log').insert_one(data)


# 对project做指定操作
def add_project(project_name, project_description, ctime):
    data = {"project":project_name, "description":project_description, "ctime":ctime}
    get_db("project").insert_one(data)    

def read_project_name_all():
    projects = []
    for record in get_db("project").find():
        projects.append(record['project'])
    return projects

def del_project(project_name):
    get_db("project").delete_one({'project':project_name})

# 对search string做指定操作

def add_search_str(project_name, sstr, ctime): # 搜索词条专门是一个列表
    data = {"project":project_name, "sstr":sstr, "ctime":ctime}
    get_db("sstr").insert_one(data)  


def del_search_str(sstr):
    get_db("sstr").delete_one({'sstr':sstr})

def 

if __name__ == "__main__":
    print read_journal_detail('JOURNAL OF FOOD SAFETY')

