# -*- coding: utf-8 -*-
# !/usr/bin/env python
# coding:utf-8

import agents
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import utilities as ut
import config
import time

phantomjs_headers = agents.get_header() # 随机选择一个以供浏览器使用
dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap["phantomjs.page.settings.userAgent"] = (phantomjs_headers)  # header每次打开phantomjs是随机的，但浏览器关闭前不会变
dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
# browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器，windows下使用
path = ut.cur_file_dir() + "/browser/phantomjs" # 浏览器地址
browser = webdriver.PhantomJS(executable_path=path, desired_capabilities=dcap)  # 加载浏览器
browser.set_page_load_timeout(config.phantom_time_out)  # 设定网页加载超时,超过了就不加载

print browser

if browser:
    print "test1"


browser.quit()
time.sleep(5)

print browser

if browser:
    print "test2"