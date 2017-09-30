# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: init.py
   Description: 程序初始化，预读取库、数据库等
   Author: Dexter Chen
   Date：2017-09-30
-------------------------------------------------
   Development Note：
   1.
-------------------------------------------------
   Change Log:

-------------------------------------------------
"""
import mongodb_handler as mh

pmids = []

def init_sets():
    global pmids
    pmids = mh.read_pmid_all()

if __name__ == '__main__':
    init_sets()
    print pmids
