# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: citation.py
   Description: 查找文献的引用量
   Author: Dexter Chen
   Date：2017-10-26
-------------------------------------------------
"""

import re


def get_country(institute_raw_list):
    for institute_raw in institute_raw_list:
        institute_strs = institute_raw.split(',')
