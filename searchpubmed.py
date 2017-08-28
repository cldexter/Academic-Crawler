# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""
-------------------------------------------------
   File Name: search_pubmed.py      
   Description: search for defined words combination
   Author: Dexter Chen
   Date：2018-08-25
-------------------------------------------------
   Change Log:
   2018-08-25: 重写了大部分代码，使用面对对象的办法
-------------------------------------------------
"""

import sys,os,csv,re,time,schedule,requests,ctypes
from datetime import date,datetime,timedelta
from BeautifulSoup import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf8')   

projects_set = []
key_words_set = []
parameter_set = []
url_set = []#用于储存关键词生成的所有链接
record_set = []#用于临时储存需要放入csv的内容
#=========================================================================================
#把所有的对象放在下面
class Color: #打印颜色的定义，在这里做字典用
    BLACK = 0  
    BLUE = 1  
    DARKGREEN = 2  
    DARKCYAN = 3  
    DARKRED = 4  
    DARKPINK = 5  
    BROWN = 6  
    default = 7  #默认的颜色是银色
    fade = 8  #忽略用灰色表示
    BLUE = 9  
    safe = 10 #安全用绿色表示 
    CYAN = 11  
    warning = 12  #红色用于表示
    highlight = 13  #紫色用于高亮信息
    form = 14  #表格用黄色的来打
    WHITE = 15

class Watchdog: #看门狗程序，防止运行卡死 
    def __init__(self):
        ''' Class constructor. The "time" argument has the units of seconds. '''
        self._time = maxPorcessTime
        return
        
    def StartWatchdog(self):
        ''' Starts the watchdog timer. '''
        self._timer = Timer(self._time, self._WatchdogEvent)
        self._timer.daemon = True
        self._timer.start()
        return
        
    def PetWatchdog(self):
        ''' Reset watchdog timer. '''
        self.StopWatchdog()
        self.StartWatchdog()
        return
        
    def _WatchdogEvent(self):
        '''
        This internal method gets called when the timer triggers. A keyboard 
        interrupt is generated on the main thread. The watchdog timer is stopped 
        when a previous event is tripped.
        '''
        cPrint(u'\n ●调 等待太久，程序强制跳过 \n',Color.warning) 
        self.StopWatchdog()
        thread.interrupt_main()
        return

    def StopWatchdog(self):
        ''' Stops the watchdog timer. '''
        self._timer.cancel()
#=========================================================================================
#爬虫蜘蛛的作用：传入关键词，1.自动生成sum page连接 2.爬sum page 3.判断哪些要怕细节 4.爬细节 5.根据选择，决定是否储存 6.传递关键信息
class Spider:#爬虫的蜘蛛
	def __init__(self,key_words,record_number):
		self.key_words = key_words#输入关键词
		self.record_number = record_number#需要爬多少个

		#实例内部变量
		self.parameter = []
		self.url = []
		self.sum_page_url = []
		self.abstract_page_url = []
		self.output_msg = []

		#实例内部常量
		self.url = "https://www.ncbi.nlm.nih.gov/pubmed/?term="


	def sum_page_url(self):#产生sum page的url
		fork ey_word in self.key_words:
			self.parameter.append(key_words.replace(",","+"))
		
		


	def abstract_page_url():#产生蜘蛛的url
		pass

	def crawl_sum_page(self):#爬
		pass

	def crawl_abstract_page(self): #爬具体页面
		pass

	def record(self,):#记录格式是json
		pass

	def output(self,msg):#输出信息都用json格式
		pass




	


#=========================================================================================
#如下信息是需要输出的（终端或者web）
display_buffer = []

#header不要轻易该，反复测试后选择的
headers = {'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Referer':"https://www.ncbi.nlm.nih.gov/pubmed", 
"Connection": "keep-alive",
"Pragma": "max-age=0",
"Cache-Control": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6"
}

def data_read(project_name,file_type):#所有读取都用这个
	data_set = []
	with open(file_name(project_name,file_type), 'rb') as csvfile:
		data = csv.reader(csvfile, dialect='excel')
		for row in data:
			data_set.append(','.join(row))
	return data_set

def data_write(data,project_name,file_type):#所有储存都这样弄
	with open(file_name(project_name,file_type), 'a') as csvfile:
	    data_writer = csv.writer(csvfile, dialect='excel')
	    data_writer.writerow(data)
	time.sleep(0.1)

def text_read(project_name,file_type):#读取pmid库，自动关闭文件
	with open(file_name(project_name,file_type),'r') as f:
		pmid_set = f.read()
	return pmid_set

def text_write(data,project_name,file_type):#存入pmid,自动关闭文件
	with open(file_name(project_name,file_type),"a") as f:
		f.write(data +',')
	time.sleep(0.1)

def projects_read():
	global projects_set
	path = cur_file_dir() + "/" + "projects.csv"
	with open(path,"rU") as f:
		data = csv.reader(f,dialect="excel")
		for row in data:
			projects_set.append(','.join(row))

def key_words_read(project_name):
	global key_words_set
	key_words_set = []
	with open(file_name(project_name,"key_words"),'rU') as csvfile:
		data = csv.reader(csvfile, dialect='excel')
		for row in data:
			key_words_set.append(','.join(row))

def cur_file_dir():#获取脚本路径
    path = sys.path[0]
    return path

def generate_parameter():#生成变量格式
	global parameter_set
	parameter_set = []
	for key_words in key_words_set:
		parameter_set.append(key_words.replace(",","+"))

def generate_url():#生成URL
	url = "https://www.ncbi.nlm.nih.gov/pubmed/?term="
	global url_set
	url_set = []
	for parameter in parameter_set:
		url_set.append(url+parameter)

def check_folders(project_name):#检查项目文件夹是否存在，项目文件夹一定包含了项目所需文件
	path = cur_file_dir() + "/" + project_name +"/"
	b = os.path.isdir(path)
	return b

def check_pmid_record(project_name,pmid):#pmid在不在历史文件中，在，返回1；如果不在，返回0;用于防止抓多了
	pmid_set = text_read(project_name,"history")
	if pmid in pmid_set:
		return 1#如果有，说明是旧的
	else:
		return 0#如果没有，说明是新的

def generate_files(project_name):#生成文件夹以及原始文件：数据、历史、关键词
	path = cur_file_dir() + "/" + project_name +"/" 
	os.mkdir(path)#根据path生成文件夹，下面生成所有项目所需文件
	new_data_file = open(path+project_name+"_data.csv",'w')
	new_hisotry_file = open(path+project_name+"_history.txt",'w')
	new_key_words_file = open(path+project_name+"_key_words.csv",'w')
	new_data_file.close()
	new_hisotry_file.close()
	new_key_words_file.close()

def file_name(project_name,file_type):#用于查询当前的文件位置和名称
	path = cur_file_dir() + "/" + project_name +"/" 
	if file_type == "history":
		return path+project_name+"_history.txt"
	if file_type == "data":
		return path+project_name+"_data.csv"
	if file_type == "key_words":
		return path+project_name+"_key_words.csv"
	else:
		return u" ○ Error: Wrong file type"

def menu():
	global projects_set
	print u" ■ Please choose your project"
	print "   1. All Projects"
	for i in range(len(projects_set)):
		print "   " + str(i+2) + ". " + projects_set[i]
	print "   0. Test System"
	while True:
		option = raw_input(u" >>> ")
		if option == "1":
			break
		if option == "0":
			projects_set = []
			projects_set.append("test") 
			break
		if int(option) >1 and int(option) <= len(projects_set)+2:
			j = int(option) - 2
			project = projects_set[j]
			projects_set = []
			projects_set.append(project)
			break
		else:
			print u" ○ Error: Wrong input, try again."

def cPrint(msg,color): #实现彩色打印  
	ctypes.windll.Kernel32.GetStdHandle.restype = ctypes.c_ulong  
	h = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))  
	if isinstance(color, int) == False or color < 0 or color > 15:  
		color = Color.default #  
	ctypes.windll.Kernel32.SetConsoleTextAttribute(h, color)  
	print msg
	ctypes.windll.Kernel32.SetConsoleTextAttribute(h, Color.default) 

def display_terminal(msg,msg_type):#所有需要显示在屏幕上的信息
	pass

def display_web(msg,msg_type):#所有需要显示在网页上的
	pass

def display_md(msg,msg_type)

#=========================================================================================
#这里定义每个被提取元素的起始结尾
title_start_with = "linksrc=docsum_title\">"#标记查找标题开头
title_end_with = "</a>"#查找标题的结尾
journal_start_with = 'title='#查找期刊开头
journal_end_with = '\">'#查找期刊结尾


def get_sum_page(project_name,url,l): #用于抓取搜索页详细，获取所有论文的列表
	print "="*75
	print u" ■ Key words group NO." + str(l+1) + ": {" + key_words_set[l].replace('	',',')+"}"
	print "-"*75
	tries = 3
	while(tries>0):
		try:
			opener = requests.Session()
			opener.get(url,headers=headers)
			doc = opener.get(url,timeout=5,headers=headers).text
			soup = BeautifulSoup(doc)
			content = soup.findAll(name="div",attrs={"class":"rslt"})#把sc_content类的抓过来
			author = soup.findAll(name='p',attrs={"class":"desc"})#author合集
			journal = soup.findAll(name = "span",attrs={'class':'jrnl'})#期刊合集
			title = soup.findAll(name='p',attrs={"class":"title"})#名字与连接的合集
			issue = soup.findAll(name="p",attrs={'class':'details'})#年份的合集
			pmid = soup.findAll(name="dd")#Pmid的合集
			break
		except Exception,e:
			tries -=1
			print u" ○ Error: Cannot retrieve sum page, trying again; " + str(tries) + u" times left"
			time.sleep(5)
	else:
		print u" ○ Error: Sum page not available now"

	m = 0
	n = 0
	for m in range(len(content)):#有多少重复多少
		author[m] = str(author[m])[16:-4]#作者
		journal_end = str(journal[m]).find(journal_end_with)
		journal[m] = str(journal[m])[26:journal_end].replace('<b>','').replace('</b>','')#期刊
		pmid[m] = str(pmid[m])[4:-5]#pmid 
		title_start = str(title[m]).find(title_start_with) + 22
		title[m] = str(title[m])[title_start:-8].replace('<b>','').replace('</b>','')#论文名
		issue[m] = re.search("[1-2][09][0-9]{2}", str(issue[m])).group(0)#刊号
		if not(check_pmid_record(project_name,pmid[m])):#如果之前没有这篇文章
			abstract = get_abstract(pmid[m])#获取abstract
			record = author[m],issue[m],pmid[m],title[m],journal[m],abstract[0],abstract[1]
			if abstract != u"Error: Abstract not available now":#如果返回的abstract错误，不记录入历史
				data_write(record,project_name,"data")#录入数据文件
				text_write(pmid[m],project_name,"history")#录入历史文件
				n += 1 #记录多少篇新文章
				print u" ● New: " + str(title[m]) #录入
				time.sleep(5)
		else:
			print u" ○ Skipped NO." + str(m+1) + u": Already retrieved"
			time.sleep(0.5)
		if m+1 == len(content):
			pass
		else:
			print "-" * 75
	print "=" * 75
	print u" ■ Retrieved " + str(n) + u" new articles"
	
	time.sleep(5)
 
def get_abstract(pmid):#用于抓取详细页信息，获取论文的abstract, 输入pmid，返回abstract
	link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
	full_content_links = []
	full_links = []
	tries = 3#尝试获取3次，不成功就返回错误
	while(tries > 0):
		try:
			opener = requests.Session()
			doc = opener.get(link,timeout=5,headers=headers).text
			soup = BeautifulSoup(doc)
			content = soup.findAll(name="abstracttext")
			abstract = str(content)
			full_content = soup.findAll(name='div',attrs={"class":"icons portlet"})
			full_links = re.findall("<a href=.*?ref=",str(full_content))
			if full_links:
				for full_link in full_links:
					full_content_links.append(full_link[9:-6].replace("&amp;","&"))
			return abstract,full_content_links#返回的是一个值和一个集合
			break
		except Exception,e:
			tries -= 1
			print u" ○ Error: Cannot retrieve abstract; " + str(tries) + u" times left"
			time.sleep(5)
	else:
		print u" ○ Error: Abstract not available now"
		return u" ○ Error: Abstract not available now"

def run_project(project_name):#主要的工作
	key_words_read(project_name)#读取关键词
	generate_parameter()#生成索引
	generate_url()#生成url
	l = 0
	while l in range(len(url_set)):
		# os.system('clear')
		print u" ■ Project: " + project_name
		get_sum_page(project_name,url_set[l],l)
		l += 1

def main():#实际执行的
	projects_read()#读取所有项目
	menu()#根据选择决定运行哪个项目
	i = 0
	while i in range(len(projects_set)):
		# os.system(u'clear')
		if check_folders(projects_set[i]):#如果有这个项目，就进行
			run_project(projects_set[i])
		else:
			print u" □ Project folder doesn't exist, creating folders for: " + projects_set[i]
			generate_files(projects_set[i])
			raw_input(u' ■ Please edit the keywords list and press \'Continous\'...')
			run_project(projects_set[i])
		i += 1

if __name__ == '__main__':
	main()



