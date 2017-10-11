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

client = MongoClient('mongodb://localhost:27017/')  # 固定的不要变动

# 获取各个集合路径; 注意这里的db不是database，是collection
def get_db(data_type):
    if data_type in ["content", "project", "log", "task", "journal", "sstr"]:
        database = client["papers"][data_type]
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
    record = get_db("journal").find_one({"journal": journal_name})
    if record:
        data = record['journal'], record['if'], record['jzone']
    return data


def add_journal(journal_name, impact_factor, journal_zone):
    data = {"journal": journal_name,
            "if": impact_factor, "jzone": journal_zone}
    get_db("journal").insert_one(data)


# 对论文(content)指定操作部分
def read_pmid_all():
    pmids = []
    for record in get_db("content").find():
        pmids.append(record['pmid'])
    return pmids


def add_new_content(project, sstr, ctime, source, pmid, title, author, journal, ojournal, impact_factor, jzone, issue, abstract, keyword, institue, flink):  # 新增一个论文记录
    data = {"project": project, "sstr": sstr, "ctime": ctime, "status": 1, "source": source, "pmid": pmid, "title": title, "author": author, "journal": journal, "ojournal": ojournal, "if": impact_factor, "jzone": jzone,
            "issue": issue, "abstract": abstract, "keyword": keyword, "institue": institue, "irank": "", "country": "", "flink": flink, "usability": "", "relativeness": "", "quality": "", "highlight": "", "comment": ""}
    get_db("content").insert_one(data)


def update_content(pmid, new_content):  # 更新论文数据模块，注意new_content不需要双引号
    get_db("content").update_one({'pmid': pmid}, {"$set": new_content})


def del_content(pmid):
    get_db("content").delete_one({'pmid': pmid})


# 对log做制定操作
def add_new_log(task, ctime, loginfo, logtype):
    data = {"task": task, "ctime": ctime,
            "loginfo": loginfo, "logtype": logtype}
    get_db('log').insert_one(data)


# 对project做指定操作
def read_project_name_all():
    projects = []
    for record in get_db("project").find():
        projects.append(record['project'])
    return projects


def read_project_detail(project_name):
    record = get_db("project").find_one({"project": project_name})
    if record:
        data = record['project'], record['sstr'], record['type']
    return data    


def add_new_project(project_name, project_description, ctime):
    data = {"project": project_name,
            "description": project_description, "ctime": ctime}
    get_db("project").insert_one(data)


def del_project(project_name):
    get_db("project").delete_one({'project': project_name})


# 对search string做指定操作
def add_search_str(project_name, sstr, ctime, type, loop = 1, frequency = 24):  # 搜索词条专门是一个列表
    data = {"project": project_name, "sstr": sstr, "ctime": ctime, "type": type, "loop": loop, "frequency": frequency}
    get_db("sstr").insert_one(data)


def del_search_str(project_name, sstr):
    get_db("sstr").delete_one({"project": project_name, 'sstr': sstr})


def read_search_str_all(project_name):
    sstr = []
    for record in get_db("sstr").find({"project": project_name}):
        sstr.append(record['sstr'], record['ctime'], record['type'], record['loop'], record['frequency'])
    return sstr 

def count_search_str(project_name):
    number = get_db('sstr').count({"project": project_name})
    return number


# 对task做指定操作
def add_new_task(project_name, sstr, ctime, itemnum, mrhours, endwith = 0, status = 0):  # 搜索词条专门是一个列表
    data = {"project": project_name, "sstr": sstr,"ctime": ctime, "itemnum": itemnum, "mrhours": mrhours, "endwith": endwith, "status": status}
    get_db("task").insert_one(data)

def count_task(project_name, sstr):
    number = get_db("task").count({"project": project_name, "sstr": sstr})
    return number



if __name__ == "__main__":
    # add_new_project("cancer", "aim to find the latest cancer research progress", "2017-10-10 10:10:10")
    add_new_task("cancer", "breast,cancer", "2017-10-10 10:10:10", 5000, 6, 0, 0)
    print count_task("cancer", "breast,cancer")