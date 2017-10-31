# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: stats.py
   Description: 运行统计数据
   Author: Dexter Chen
   Date：2017-09-19
-------------------------------------------------
   Development Note：
   1. 根据log，生成统计文件
   2. 对关键词等信息
-------------------------------------------------
   Change Log:
   2018-08-31: 
-------------------------------------------------
"""

import config


processed_sum_page = 0
processed_record = 0
processed_pmid = 0
success_sum_page = 0
success_record = 0
success_pmid = 0
failed_sum_page = 0
failed_record = 0
failed_pmid = 0
skipped_sum_page = 0
skipped_record = 0
skipped_pmid = 0
c_skipped_pmid = 0

crawl_pmid_start = ""
crawl_pmid_finish = ""
crawl_detail_start = ""
crawl_detail_finish = ""


def last_task_duration(project, sstr):
    pass

def c_skipped_pmid_counter(result):
    global c_skipped_pmid
    if result == "skip":
        c_skipped_pmid += 1
    elif result == "succ":
        c_skipped_pmid = 0
    if c_skipped_pmid >= config.pmid_max_c_skip:
        return False
    else:
        return True


if __name__ == '__main__':
    i = 0
    while i < 5:
        print c_skipped_pmid_counter("skip") 
        i += 1
    print c_skipped_pmid_counter("succ")