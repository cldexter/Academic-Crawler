# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: config.py
   Description: 静态设置
   Author: Dexter Chen
   Date：2017-10-11
-------------------------------------------------
"""
display_protocol = 5  # 定义哪种显示方法
log_protocol = 2  # 定义哪种记录方法

request_time_out = 30  # request超时时间
phantom_time_out = 60  # phantom超时时间

request_refresh_wait = 3  # request刷新等待
phantom_refresh_wait = 10  # phantom刷新等待

phantom_sp_wait = 10 # 使用phantom抓取sum时每页的等待时间（反反爬虫）

request_dp_tries = 3  # 使用request抓取dp最多尝试次数
request_sp_tries = 3  # 使用request抓取sp最多尝试次数

phantom_1st_sp_tries = 3  # 尝试获取第一个sp的次数
phantom_other_sp_tries = 5  # 尝试获取其它每个sp的次数

detail_crawler_number = 10  # 多线程爬虫数量

proxy_max_fail = 30  # 准许每个代理IP最多失败次数
proxy_max_c_fail = 3  # 准许每个代理连续失败次数
proxy_max_used = 2000  # 一天内最大的使用次数
proxy_pool_size = 3  # 代理池里面的IP数量

pmid_max_c_skip = 3  # 在任务提前完成中，准许连续跳开的pmid数
