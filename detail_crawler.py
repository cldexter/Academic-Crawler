# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: detail_crawler.py
   Description: 蜘蛛类，只爬pubmed的详细页
   Author: Dexter Chen
   Date：2017-10-10
-------------------------------------------------
"""

import sys
import re
import time

import requests
from lxml import etree  

import agents
import mongodb_handler as mh
import journal as jn
import utilities as ut
import message as msg
import stats
import config


# def generate_record(self):  # 从抓取的原始素材产生记录
#     title_start_with = "linksrc=docsum_title\">"  # 标记查找标题开头
#     title_end_with = "</a>"  # 查找标题的结尾
#     journal_start_with = 'title='  # 查找期刊开头
#     journal_end_with = '\">'  # 查找期刊结尾
    
#     m = 0
#     while(m < len(self.pmid)):  # 有多少重复多少
#         pmid = str(self.pmid[m])[4:-5]  # 先找到pmid，再决定要不要下一步
#         if not(self.pmid_check(pmid)):  # 如果之前没有这篇文章
#             author = str(self.author[m])[16:-4]
#             author_list =  author.split(", ") # 作者列表

#             title_start = str(self.title[m]).find(title_start_with) + 22
#             title = str(self.title[m])[title_start:-8].replace('<b>', '').replace('</b>', '')  # 论文名

#             issue = re.search("[1-2][09][0-9]{2}", str(self.issue[m])).group(0)  # 刊号，即年份

#             journal_end = str(self.journal[m]).find(journal_end_with)  # 期刊结尾位置
#             journal = str(self.journal[m])[26:journal_end].replace('<b>', '').replace('</b>', '')  # 期刊名
#             journal_detail = jn.journal_detail(journal) # 获取期刊的正式名称，影响因子及分区信息

#             paper_detail = self.crawl_detail(pmid)  # 获取文章abstract，keyword列表，机构列表和全文链接列表

#             if paper_detail:  # 如果能够返回正确的abstract，记录；否则留给下一次抓取（不记录，视作新论文）
#                 mh.add_new_content(self.project_name, self.key_words, ut.time_str("full"), "pm", pmid, title, author_list, journal, journal_detail[0], journal_detail[1], journal_detail[2], issue, str(paper_detail[0]), paper_detail[1], paper_detail[2], paper_detail[3])
#                 self.pmid_set.append(pmid) # 把刚抓的这篇pmid加入pmid list
#                 #这里的 paper_detail[0]是这篇文章的abstract,[1]是keywords,[2]是机构列表 [4]是全文下载的链接合集


#         else:
#             pass
#         m += 1    

def crawl_detail(pmid):  # 爬具体页面   
    link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
    # key_words_list = []  # 关键词合集
    # institues_list = []  # 机构名称
    # full_links_list = []  # 全文链接（不是abstract，是可下载的pdf）


    tries = 1  # 尝试获取3次，不成功就返回错误
    while(tries > 0):
        try:
            opener = requests.Session() # 新建了session保存
            content = opener.get(link, timeout=config.request_time_out, headers=agents.get_header()).text # 注意，这里是不断随机换agent的
            selector = etree.HTML(content.encode("utf-8"))

            title_element = selector.xpath("//div[@class = \"rprt abstract\"]//h1")
            if len(title_element):
                title = title_element[0].xpath('string(.)')

            author_element = selector.xpath("//div[@class = \"auths\"]//a")
            authors = []
            if len(author_element):
                for author in author_element:
                    authors.append(author.xpath('string(.)'))

            abstract_element = selector.xpath("//*[@id=\"maincontent\"]/div/div[5]/div/div[4]")
            if len(abstract_element):
                abstract = abstract_element[0].xpath('string(.)')[8:]

            key_words_element = selector.xpath("//*[@id=\"maincontent\"]/div/div[5]/div/div[5]/p")
            if len(key_words_element):
                key_words = key_words_element[0].xpath('string(.)').split("; ")
            else:
                key_words = []

            issue_element = selector.xpath("//div[@class = \"cit\"]")
            if len(issue_element):
                issue = issue_element[0].xpath('string(.)')

            institues_element = selector.xpath("//div[@class=\"afflist\"]//dd")
            institues = []
            if len(institues_element):
                for institue in institues_element:
                    institues.append(institue.xpath('string(.)'))
            
            flink_element = selector.xpath("//div[@class=\"icons portlet\"]//a/@href")
            flinks = []
            if len(flink_element):
                for flink in flink_element:
                    flinks.append(flink)
            
            print issue

            
            break
        
        except Exception, e:
            print e
            tries -= 1
            time.sleep(config.request_refresh_wait)  # 如果抓不成功，就先休息3秒钟
    
    else:
        print "error"
        return 0

if __name__ == '__main__':
    crawl_detail("28538041")