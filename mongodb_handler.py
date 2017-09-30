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
   1.与data_handler的功能、函数名一致，可以直接替代
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

my_record = {"pmid":"200000", "name": "dexter", "hello": "world"}

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


# 对论文指定操作部分

def read_pmid_all():
    pmids = []
    for record in get_db("content").find():
        pmids.append(record['pmid'])
    return pmids


def update_content(pmid, new_content):  # 更新论文数据模块，注意new_content不需要双引号
    get_db("content").update_one({'pmid': pmid}, {"$set": new_content})


def del_content(pmid):
    get_db("content").delete_one({'pmid': pmid})


if __name__ == "__main__":
    pass