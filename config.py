# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: config.py
   Description: 所有静态设置都搬到这里
   Author: Dexter Chen
   Date：2017-10-11
-------------------------------------------------
"""

request_time_out = 30 # request超时时间
phantom_time_out = 60 # phantom超时时间
request_refresh_wait = 3 # request刷新等待
phantom_refresh_wait = 5 # phantom刷新等待
request_dp_tries = 3 # 使用request抓取dp最多尝试次数
request_sp_tries = 3 # 使用request抓取sp最多尝试次数
phantom_1st_sp_tries = 3  # 尝试获取第一个sp的次数
phantom_other_sp_tries = 5  # 尝试获取其它每个sp的次数