#! /usr/bin/env python
# coding=utf-8
# -*- coding:utf-8 -*-

import sys,os,time,schedule,re,csv
import requests
from BeautifulSoup import BeautifulSoup

#header不要轻易该，反复测试后选择的
headers = {'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Referer':"http://gz.centanet.com/ershoufang/t1/?key=%e5%b9%bf%e5%b7%9e", 
"Connection": "keep-alive",
"Pragma": "max-age=0",
"Cache-Control": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6"
}

url_begin = "http://gz.centanet.com/ershoufang/t1"
url_end = "/?key=%E5%B9%BF%E5%B7%9E"
url_set = []
detail_set = []

reload(sys) 
sys.setdefaultencoding('utf8')  

def cur_file_dir():#获取脚本路径
    path = sys.path[0]
    return path

def file_name(file_type):#用于查询当前的文件位置和名称
	path = cur_file_dir() + "/" + "resource" +"/" 
	if file_type == "apartment":
		return path+"apt.txt"
	if file_type == "history":
		return path+"history.csv"
	else:
		return u" ○ Error: Wrong file type"

def data_read(file_type):#所有读取都用这个
	data_set = []
	with open(file_name(file_type), 'rb') as csvfile:
		data = csv.reader(csvfile, dialect='excel')
		for row in data:
			data_set.append(','.join(row))
	return data_set

def data_write(data,file_type):#所有储存都这样弄
	with open(file_name(file_type), 'a') as csvfile:
	    data_writer = csv.writer(csvfile)
	    data_writer.writerow(data)
        print "done!"

def generate_url():
    global url_set
    url = url_begin + url_end
    opener = requests.Session()
    opener.get(url,headers=headers)
    doc = opener.get(url,timeout=5,headers=headers).text
    soup = BeautifulSoup(doc)
    content = soup.findAll(name="span",attrs={"class":"fred fTahoma"})
    total_number = str(content[0])[27:-7]
    page_number = int(total_number)/25 + 1
    i = 0
    for i in range(0,page_number):
        url_each = url_begin + "g" + str(i+1) + url_end
        url_set.append(url_each)

def generate_detail(url):
    global detail_set
    opener = requests.Session()
    opener.get(url,headers=headers)
    doc = opener.get(url,timeout=5,headers=headers).text
    soup = BeautifulSoup(doc)
    content = soup.findAll(name="div",attrs={"class":"house-item clearfix"})
    i = 0
    for i in range(0,len(content)):
        content_str = str(content[i])
# 以下是抓取位置，根据网页变化可能需要定期修订（2017-08-23）
        describe_begin = content_str.find('cBlueB') + 15
        describe_end = content_str.find('_blank',describe_begin) - 10
        type_begin = content_str.find('<span>',describe_end) + 6
        type_end = content_str.find('</span>',type_begin)
        area_begin = content_str.find('<span>',type_end) + 6
        area_end = content_str.find('</span>',area_begin) - 4
        flo_begin = content_str.find('<p class="house-txt"><span>') + 27
        flo_end = content_str.find('</span>',flo_begin)
        dir_begin = content_str.find('<span>',flo_end) + 6
        dir_end = content_str.find('</span>',dir_begin)
        dec_begin = content_str.find('<span>',dir_end) + 6
        dec_end = content_str.find('</span>',dec_begin)
        year_begin = content_str.find('<span>',dec_end) + 6
        year_end = content_str.find('</span>',year_begin)
        loc_begin = content_str.find('<span>',year_end) + 6
        loc_end = content_str.find('</span>',loc_begin)
        pri_begin = content_str.find('price-nub') + 26
        pri_end = content_str.find('</span>',pri_begin)
        pria_begin = content_str.find('price-txt') + 14
        pria_end = content_str.find('</p>',pria_begin) - 7
        prib_begin = content_str.find('price-txtB') + 53
        prib_end = content_str.find('</p>',prib_begin) - 7
#以下是抓取内容，不需要修订
        id = str(content_str[9:45])
        # print id
        describe = str(content_str[describe_begin:describe_end])
        # print describe
        apt_type = str(content_str[type_begin:type_end])
        # print apt_type
        area = str(content_str[area_begin:area_end])
        # print area
        floor = str(content_str[flo_begin:flo_end])
        # print floor
        direction = content_str[dir_begin:dir_end]
        # print direction
        decoration = content_str[dec_begin:dec_end]
        # print decoration
        year = content_str[year_begin:year_end]
        # print year
        location = content_str[loc_begin:loc_end]
        # print location
        total_price = content_str[pri_begin:pri_end]
        # print total_price
        average_price = content_str[pria_begin:pria_end]
        # print average_price
        local_price = content_str[prib_begin:prib_end]
        # print local_price
        record = "(" + describe +','+ floor +','+ direction +','+ decoration +','+ year +','+ location +','+ total_price +','+ average_price +','+ local_price + ")"
        detail_set.append(record)
        # print record
def main():
    generate_detail("http://gz.centanet.com/ershoufang/t1g2/?key=%E5%B9%BF%E5%B7%9E")
    print detail_set.encode('gbk')
    data_write(detail_set,"history")

if __name__ == '__main__':
    main()
    
    # print detail_set
