# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: data_operate.py
   Description: 处理与影响因子及文章分区相关查询
   Author: Dexter Chen
   Date：2017-09-09
-------------------------------------------------
   Development Note：
   1. 查询杂志的标准缩写
   2. 查询杂志N年内的影响因子
   3. 查询杂志分区信息
   4. 储存并调用已查询过的信息
-------------------------------------------------
   Change Log:
   2018-09-14: 重新复活 
-------------------------------------------------
"""

from __future__ import division # python除法变来变去的，这句必须放开头
import time
import sys
import math
import json
import requests
import re
import csv

reload(sys)
sys.setdefaultencoding('utf8')

# 查找杂志的全名
def search_full_name(journal_name):
    url = "http://www.letpub.com.cn/journalappAjax.php?querytype=autojournal&term=" + journal_name.replace(" ","+")
    