# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: proxy.py
   Description: 自动从大象代理获得代理IP
   Author: Dexter Chen
   Date：2017-09-16
-------------------------------------------------
"""

import os
import requests
import utilities as ut
import config


def retrieve_proxy(proxy_number):
    api_url = "http://vtp.daxiangdaili.com/ip/?tid=559131754091145&num=" + \
        str(proxy_number) + "&delay=1&sortby=time"
    proxies = requests.get(api_url, timeout=10).text
    proxy_pool = []
    for proxy in proxies.split("\n"):
        proxy_record = ut.time_str("full"), proxy, 0, 0, 0
        proxy_pool.append(proxy_record)
    return proxy_pool


def is_usable(proxy_record):  # 检测是否还能那个用
    if int(proxy_record[2]) < config.proxy_max_used and int(proxy_record[3]) < config.proxy_max_fail and proxy_record[4] < config.proxy_max_c_fail:  # 超出最大量、连续最多失败次、失败总次数都要了
        return True
    else:
        return False


def update_pool(proxy_pool):
    if len(proxy_pool):
        proxy_pool = filter(is_usable, proxy_pool)
    if len(proxy_pool) < config.proxy_pool_size:
        retrieve_proxy(proxy_pool_size - len(proxy_pool))  # 缺多少，补多少
    proxy_pool = sorted(proxy_pool, key=lambda x: x[2])  # 按照使用次数排序，用的最少的最先用
    return proxy_pool


def is_online():
    status = os.system("ping -c 1 www.163.com")
    if status == 0:
        return True
    else:
        return False


def get_proxy():  # 这里是在程序中获得proxy
    proxy_pool = update_pool(proxy_pool)
    proxy_pool[0][2] += 1  # 增加用了1次
    return proxy_pool[0][1]


if __name__ == '__main__':
    print retrieve_proxy(1)
