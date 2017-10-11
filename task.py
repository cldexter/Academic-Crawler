# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: task.py
   Description: 生成任务列表
   Author: Dexter Chen
   Date：2017-10-11
-------------------------------------------------
   Development Note：
   1. 根据选择，确定需要执行的项目及细节
   2. 根据之前的统计，确定
   2. 将制定好的时间表，放入csv文件
   3. 按照时间表执行
   4. 监控执行情况，实时统计
   5. 看门狗程序，必要时重启
   6. 记录运行出现的问题
-------------------------------------------------
"""

from datetime import date, datetime, timedelta
import mongodb_handler as mh
import utilities as ut


task_list = []

def generate_task_config(project_name, sstr):
    sstr_number = mh.count_search_str(project_name) #一共有多少个sstr
    task_number = mh.count_task(project_name, sstr) #本sstr运行过多少次
    if sstr_number <= 1: # 如果这个是第一个sstr
        endwith = 0 # 不提前终止
        else:
            endwith =1 # 按条件提前终止
    if task_number <= 1: # 如果是第一次运行
        mrhours = 6 # 单位是小时
        itemnum = 5000
        else:
            mrhours = 0.1
            itemnum = 20
    return itemnum, mrhours, endwith #  返回了一个列表

def generate_tasks(project_name, sstr):
    config = generate_task_config(project_name, sstr)
    mh.add_new_task(project_name, sstr, ut.time_str("full"), config[0], config[1], config[2], 0)








def generate_task_list(): # 项目名称，第一个项目几小时后开始，项目间最小间隔
    pass

def run_task(startTime, loopTime):  # 多少时间后开始运行
    pass





if __name__ == '__main__':
    pass
