# -*- coding: utf-8 -*-
# !/usr/bin/env python

import time,sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from BeautifulSoup import BeautifulSoup
#header不要轻易该，反复测试后选择的
headers = {'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Referer': "https://www.ncbi.nlm.nih.gov/pubmed",
"Connection": "keep-alive",
"Pragma": "max-age=0",
"Cache-Control": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6"
}
opener = requests.Session()
opener.get("https://www.ncbi.nlm.nih.gov/pubmed/?term=dexter+chen",headers=headers)
doc = opener.get("https://www.ncbi.nlm.nih.gov/pubmed/?term=dexter+chen",timeout=5,headers=headers).text
soup = BeautifulSoup(doc)
content = soup.findAll(name="div",attrs={"class":"rslt"}) #把sc_content类的抓过来
# author = soup.findAll(name='p',attrs={"class":"desc"})#author合集
# journal = soup.findAll(name = "span",attrs={'class':'jrnl'})#期刊合集
# title = soup.findAll(name='p',attrs={"class":"title"})#名字与连接的合集
# issue = soup.findAll(name="p",attrs={'class':'details'})#年份的合集
pmid = soup.findAll(name="dd")#Pmid的合集
print pmid