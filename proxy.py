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

import os
import requests
import utilities as ut

proxy_pool = []  # 每个proxy = 获得时间、最后一次成功使用时间、使用次数、失败次数

max_fail = 30  # 准许每个代理IP最多失败次数
max_c_fail = 3 # 准许每个代理连续失败次数
max_used = 2000  # 一天内最大的使用次数
proxy_pool_size = 3  # 代理池里面的IP数量


def retrieve_proxy(proxy_number):
    api_url = "http://vtp.daxiangdaili.com/ip/?tid=559131754091145&num=" + \
        str(proxy_number) + "&delay=1&sortby=time"
    proxies = requests.get(api_url, timeout=10).text
    for proxy in proxies.split("\n"):
        proxy_record = ut.time_str("full"), proxy, 0, 0, 0
        proxy_pool.append(proxy_record)


def is_usable(proxy_record):  # 检测是否还能那个用
    if int(proxy_record[2]) < max_used and proxy_record[3] < max_fail and proxy_record[4] < max_c_fail: # 超出最大量、连续最多失败次、失败总次数都要了
        return True
    else:
        return False


def update_pool():
    global proxy_pool
    proxy_pool = filter(is_usable, proxy_pool)
    if len(proxy_pool) < proxy_pool_size:
        retrieve_proxy(proxy_pool_size - len(proxy_pool))  # 缺多少，补多少
    proxy_pool = sorted(proxy_pool, key=lambda x: x[2])  # 按照使用次数排序，用的最少的最先用


def is_online():
    status = os.system("ping -c 1 www.163.com")
    if status == 0:
        return True
    else:
        return False

def get_proxy(): # 这里是在程序中获得proxy
    update_pool()
    proxy_pool[0][2] += 1 # 增加用了1次
    return proxy_pool[0]


if __name__ == '__main__':
    is_online()