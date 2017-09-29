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
   格式：
-------------------------------------------------
"""
import os
import sys
from pymongo import *

reload(sys)
sys.setdefaultencoding('utf8')

my_record = {"name":"dexter","hello":"world"}

def get_db():
    client = MongoClient('mongodb://localhost:27017/')
    my_table = client.myFirstMB.create_collection('dexter')
    return my_table

def add_string(my_table):
    my_table.insert(my_record)
    
def get_str(my_collection):
    print my_collection

if __name__ == "__main__":
