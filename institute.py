# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: institute.py
   Description: 有关机构相关
   Author: Dexter Chen
   Date：2017-10-26
-------------------------------------------------
"""

import re
import utilities as ut
import dictionary


institute_raw_list = [
        "Department of Biochemistry, Zhejiang University, Hangzhou 310058, PR China.", 
        "Department of Thoracic Surgery, First Affiliated Hospital, Zhejiang University, Hangzhou 310058, PR China.", 
        "Department of Pharmacology, School of Medicine, Zhejiang University, Hangzhou 310058, PR China."
]


def get_country(institute_raw_list):
    institue = []
    country = []
    for institute_raw in institute_raw_list:
        institute_raw = ut.regexp_replace(
            institute_raw, ut.re_email_pm)  # 去除pm的email语句
        institute_raw = ut.regexp_replace(
            institute_raw, ut.re_email_general)  # 去除所有中间的email
        institue.append(institute_raw)
        institute_raw = institute_raw.replace(
            ", ", ",").replace(" ,", ",").replace(".", "")  # 去除
        print institute_raw
        institute_strs = institute_raw.split(',')
        print institute_strs
        institute_strs.reverse() # 翻转序列
        print institute_strs
        i = 0
        while i < len(institute_strs):
            if institute_strs[i] in dictionary.country_names.keys():
                country_name = dictionary.country_names[institute_strs[i]]
                if not country_name in country:
                    country.append(country_name)
                break
            else:
                i += 1
        else:
            i = 0
            while i < len(inst)
    return institue, country


print get_country(institute_raw_list)


