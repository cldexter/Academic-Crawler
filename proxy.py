# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: proxy.py
   Description: 自动从大象代理获得代理IP
   Author: Dexter Chen
   Date：2017-09-16
-------------------------------------------------
   Development Note：
   1. 使用大象代理 http://www.daxiangdaili.com/
   2. 有效期至 2018-03-17 13:28
   3. 获取5个代理，循环使用，如果一次不行，计1，10次不行就
   删除，删除多少就补充多少代理
   4. 
-------------------------------------------------
"""

import requests
import utilities as ut

proxy_pool = [] # 每个proxy = 获得时间、最后一次成功使用时间、使用次数、失败次数

max_tried = 10 # 准许每个代理IP最多失败次数
max_used = 1000 # 一天内最大的使用次数
proxy_pool_size = 5 # 代理池里面的IP数量

def get_proxy(proxy_number):
    api_url = "http://vtp.daxiangdaili.com/ip/?tid=559131754091145&num=" + str(proxy_number) + "&delay=1&sortby=time"
    proxies = requests.get(api_url, timeout=10).text
    for proxy in proxies.split("\n"):
        if 
        proxy_str = ut.time_str("full"),"",proxy,0,0
        proxy_pool.append(proxy_str)

def is_usable(proxy_record): # 检测是否还能那个用
    if int(proxy_record[3]) > max_tried:
        return False
    else:
        return True

def is_not_overused(proxy_record): # 检测是否用太多了
    if int(proxy_record[2]) > max_used:
        return False # 大于最大限制，抛弃不用
    else:
        return True

def update_pool():
    global proxy_pool
    proxy_pool = filter(is_usable, proxy_pool)
    proxy_pool = filter(is_not_overused, proxy_pool)
    if len(proxy_pool) < proxy_pool_size:
        get_proxy(proxy_pool_size - len(proxy_pool)) # 缺多少，补多少
    proxy_pool = sorted(proxy_pool, key = lambda x:x[2]) # 按照使用次数排序，用的最少的最先用

def 

if __name__ == '__main__':
    print get_proxy(2)