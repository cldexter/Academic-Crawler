# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: task.py
   Description: 处理运行任务
   Author: Dexter Chen
   Date：2017-09-16
-------------------------------------------------
   Development Note：
   1. 根据选择，确定程序执行时间（时间表）
   2. 将制定好的时间表，放入csv文件
   3. 按照时间表执行
   4. 监控执行情况，实时统计
   5. 看门狗程序，必要时重启
   6. 记录运行出现的问题
-------------------------------------------------
   Change Log:
   2018-09-16: 
-------------------------------------------------
"""
import sys
import os
import data_handler as dh
import utilities

reload(sys)  
sys.setdefaultencoding('utf8')


if __name__ == '__main__':
    print project_read()
    # print project_name()
