# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: utilities.py
   Description: 多次用到的小工具
   Author: Dexter Chen
   Date：2017-09-14
-------------------------------------------------
   Development Note：
   1. 时间戳
   2. 
-------------------------------------------------
   Change Log:
   2018-09-14: 复活，把operator改为handler 
-------------------------------------------------
"""

import time

def time_now():  # 输出时间
    ISOTIMEFORMAT = '%Y-%m-%d %X'  # 设定了时间格式
    return time.strftime(ISOTIMEFORMAT, time.localtime())
