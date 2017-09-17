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
   1. 时间戳：统一用日期 + 时间的形式
   2. 显示：屏幕只显示时间，不现实日期
-------------------------------------------------
   Change Log:
   2017-09-14: 复活，把operator改为handler
   2017-09-17: 更新时间工具，可以计算后续多少小时
-------------------------------------------------
"""

import datetime

# 输出时间，带日期和不带; hr_delta 是往后数多少小时，负数往前数
def time_str(type="full", hr_delta=0):  
    if type == "full":  # 完整时间
        time_format = '%Y-%m-%d %X'
    if type == "time":  # 只有时间
        time_format = "%X"
    time_str = datetime.datetime.now()
    time = time_str + datetime.timedelta(hours=hr_delta)
    return time.strftime(time_format)

if __name__ == '__main__':
    print time_str("full")