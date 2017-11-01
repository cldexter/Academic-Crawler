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
"""

from pymongo import *
import utilities as ut

client = MongoClient('mongodb://localhost:27017/')  # 固定的不要变动
# 获取各个集合路径; 注意这里的db不是database，是collection


def get_db(data_type):
    if data_type in ["content", "project", "log", "task", "journal", "sstr", "pmid"]:
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
def read_journal_name_all():  # 读取普通名
    journals = []
    for record in get_db("journal").find():
        journals.append(record['journal'])
    return journals


def read_ojournal_name_all():  # 读取正式名称（必须是网络返回的，全大写，清洗过后的）
    ojournals = []
    for record in get_db('journal').find():
        ojournals.append(record['ojournal'])
    return ojournals


def read_journal_detail(journal_name):  # 使用普通名查询论文
    record = get_db("journal").find_one({"journal": journal_name})
    if record:
        data = record['journal'], record['ojournal'], record['if'], record['jzone']
        return data
    else:
        return 0


def read_ojournal_detail(ojournal_name):  # 使用正式名称查询论文
    record = get_db("journal").find_one({"ojournal": ojournal_name})
    if record:
        data = record['journal'], record['ojournal'], record['if'], record['jzone']
        return data
    else:
        return 0


def add_journal(journal_name, ojournal_name, impact_factor, journal_zone):
    data = {"journal": journal_name, "ojournal": ojournal_name,
            "if": impact_factor, "jzone": journal_zone}
    get_db("journal").insert_one(data)


# 对论文(content)指定操作部分
def read_pmid_all(project):  # 读取本项目所有pmid
    pmids = []
    for record in get_db("content").find({"project": project}):
        pmids.append(record['pmid'])
    return pmids


def add_new_pmid(project, sstr, ctime, source, pmid):  # 第一轮只抓取pmid，生成记录
    data = {"project": project, "sstr": sstr, "ctime": ctime,
            "status": 1, "source": source, "pmid": pmid}
    get_db("content").insert_one(data)


def add_new_pmid_many(project, sstr, ctime, source, pmid_list):  # 同时生成多个pmid记录
    data_list = []
    for pmid in pmid_list:
        data = {"project": project, "sstr": sstr, "ctime": ctime,
                "status": 1, "source": source, "pmid": pmid}
        data_list.append(data)
    get_db("content").insert_many(data_list)


def read_empty_pmid(project, sstr, pmid_number):  # 读取只有pmid，无内容的pmid以供抓取
    pmids = []
    for record in get_db("content").find({"project": project, "sstr": sstr, "status": 1}).limit(pmid_number):
        pmids.append(record['pmid'])
    return pmids


def add_new_content(pmid, title, author, journal, ojournal, impact_factor, jzone, issue, abstract, keyword, institue, country, flink):  # 实际上是把之前pmid的记录更新了
    data = {"status": 2, "title": title, "author": author, "journal": journal, "ojournal": ojournal, "if": impact_factor, "jzone": jzone,
            "issue": issue, "abstract": abstract, "keyword": keyword, "institue": institue, "irank": "", "country": country, "flink": flink}
    get_db("content").update_one({'pmid': str(pmid)}, {"$set": data})


def add_new_comments(pmid, quality, usefulness, highlight, comment):  # 实际上是把之前pmid的记录更新了
    data = {"quality": quality, "usefulness": usefulness,
            "highlight": highlight, "comment": comment}
    get_db("content").update_one({'pmid': str(pmid)}, {"$set": data})


def read_content(project, sstr, number):
    content = []
    for record in get_db("content").find({"project": project, "sstr": sstr}).limit(number):
        content.append(record)
    return content


def del_content(pmid):
    get_db("content").delete_one({'pmid': str(pmid)})


# 对log做制定操作
def add_new_log(when, who, identifier, action, result, info_type):
    data = {"ctime": when, "who": who, "identifier": identifier,
            "action": action, "result": result, "info_type": info_type}
    get_db('log').insert_one(data)


# 对project做指定操作
def read_project_all():
    projects = []
    for record in get_db("project").find():
        projects.append(record['project'])
    return projects


def read_project_detail(project):
    record = get_db("project").find_one({"project": project})
    if record:
        data = record['project'], record['sstr'], record['type']
    return data


def add_new_project(project, project_description, ctime):
    data = {"project": project,
            "description": project_description, "ctime": ctime}
    get_db("project").insert_one(data)


def del_project(project):
    get_db("project").delete_one({'project': project})


# 对search string做指定操作
def add_new_sstr(project, sstr, ctime, type, loop=1, frequency=24):  # 搜索词条专门是一个列表
    data = {"project": project, "sstr": sstr, "ctime": ctime,
            "type": type, "loop": loop, "frequency": frequency}
    get_db("sstr").insert_one(data)


def del_sstr(project, sstr):
    get_db("sstr").delete_one({"project": project, 'sstr': sstr})


def read_sstr_type(project, sstr):
    detail = get_db("sstr").find_one({"project": project, "sstr": sstr})
    if detail:
        data = detail["type"]
    else:
        data = ""
    return data


def read_sstr_all(project):
    sstr = []
    for record in get_db("sstr").find({"project": project}):
        sstr.append(record['sstr'], record['ctime'],
                    record['type'], record['loop'], record['frequency'])
    return sstr


def count_sstr(project):
    number = get_db('sstr').count({"project": project})
    return number


# 对task做指定操作
def add_new_task(project, sstr, ctime, itemnum, mrhours, endwith=0, status=0):  # 搜索词条专门是一个列表
    data = {"project": project, "sstr": sstr, "ctime": ctime, "itemnum": itemnum,
            "mrhours": mrhours, "endwith": endwith, "status": status}
    get_db("task").insert_one(data)


def count_task(project, sstr):
    number = get_db("task").count({"project": project, "sstr": sstr})
    return number


def count_project_task(project):  # 数一下该项目下运行过多少task
    number = get_db("task").count({"project": project})
    return number


def finish_task(project, sstr):  # 把任务标记为完成
    data = {"status": 1}
    get_db("task").update_one(
        {"project": project, "sstr": sstr}, {"$set": data})


if __name__ == "__main__":
    # add_new_project("organ on chip", "organ simulator, organ on chip", ut.time_str("full"))
    add_new_sstr("cancer", "liver,cancer", ut.time_str("full"), "key_words")
    # add_new_task("cancer", "breast,cancer", "2017-10-10 10:10:10", 5000, 6, 0, 0)
    # finish_task("cancer", "breast,cancer")
    # print count_task("cancer", "breast,cancer")
    # add_new_pmid("cancer", "lung,cancer", "2017-10-10 10:10:10", "pm", 29027110)
    # print read_empty_pmid("organ on chip", 10000)
    # print read_content("cancer", "lung,cancer", 1)
    # pass
