# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: output.py
   Description: 所有输出的处理
   Author: Dexter Chen
   Date：2017-09-01
-------------------------------------------------
   Development Note：
   1.处理待输出信息json
   2.在屏幕上打印
   3.输出成MD文件
   4.通过网络访问
-------------------------------------------------
   Change Log:
   2018-08-31: 建立输出方法：获取json，正确输出到屏幕 
-------------------------------------------------
"""
from __future__ import division # python除法变来变去的，这句必须放开头
import sys
import os
import json
import time
import ctypes
from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf8')

class Color: #打印颜色的定义，在这里做字典用
    BLACK = 0  
    BLUE = 1  
    DARKGREEN = 2  
    DARKCYAN = 3  
    DARKRED = 4  
    DARKPINK = 5  
    BROWN = 6  
    default = 14  #默认的颜色是黄色
    fade = 8  #忽略用灰色表示
    BLUE = 9  
    safe = 10 #安全用绿色表示 
    CYAN = 11  
    warning = 12  #红色用于表示
    highlight = 13  #紫色用于高亮信息
    form = 7  #表格用白色的来打
    WHITE = 15

def Logo():
    cPrint(u"    ■      ■                      ■                    ■                    ■  ■■■■■                ■ ", Color.form)
    cPrint(u"    ■    ■    ■■■            ■  ■            ■■■    ■■■■    ■■■    ■      ■      ■■■■■■■■■■ ", Color.form)
    cPrint(u"    ■  ■■■  ■  ■          ■      ■          ■              ■        ■    ■      ■      ■", Color.form)
    cPrint(u"  ■■■■  ■  ■  ■        ■          ■        ■■■■  ■■■■        ■    ■■■■■      ■  ■■■■■■■", Color.form)
    cPrint(u"    ■  ■■■■    ■■  ■■              ■■    ■              ■    ■■■■                  ■            ■", Color.form)
    cPrint(u"    ■  ■  ■                ■■■■■■          ■■■■■■■■■        ■    ■■■■■      ■    ■■  ■", Color.form)
    cPrint(u"    ■■■■■  ■■■        ■        ■          ■      ■    ■        ■■■      ■          ■        ■", Color.form)
    cPrint(u"  ■■  ■  ■  ■  ■        ■        ■          ■■    ■■  ■        ■■  ■    ■          ■■■■■■■■■■", Color.form)
    cPrint(u"    ■  ■■■  ■  ■        ■        ■          ■      ■    ■      ■  ■    ■■■■■      ■        ■      ■", Color.form)
    cPrint(u"    ■  ■  ■    ■          ■    ■■    ■      ■■    ■■  ■  ■      ■        ■          ■        ■    ■", Color.form)
    cPrint(u"    ■  ■  ■  ■  ■        ■            ■      ■      ■      ■■      ■        ■          ■        ■", Color.form)
    cPrint(u"  ■■■  ■■■      ■        ■■■■■■■      ■■    ■■      ■      ■  ■■■■■■■  ■        ■■            [v0.9]", Color.form)
    print "\n"

def cPrint(info,color): #实现彩色打印  
    ctypes.windll.Kernel32.GetStdHandle.restype = ctypes.c_ulong  
    h = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))  
    if isinstance(color, int) == False or color < 0 or color > 15:  
        color = Color.default #  
    ctypes.windll.Kernel32.SetConsoleTextAttribute(h, color)  
    print info
    ctypes.windll.Kernel32.SetConsoleTextAttribute(h, Color.form) # 自动回复到银色

class Output():
    def __init__(self,info,info_type):#
        self.info = info
        self.info_type = info_type

        self.color_code = {"default":14,"fade":8,"menu":15,"warning":12,"highlight":11,"safe":10}
        self.label_code = {"default":" MESSAGE","fade":"LOG-INFO","menu":" OPTION ","warning":" CAUTION","safe":" NORMAL ","highlight":" NOTICE "}

    def read_json(self):#当info是json的时候
        msg = json.dumps(self.info)
        print msg
    
    def msg_box(self):
        box_length = 85
        info = self.info
        msg_length = len(info)
        if msg_length + 44 > box_length:
            info = info[0:box_length-39] + "..."
        msg_length = len(info)    
        spaces = "  " * (box_length - msg_length -44)
        bars = "─" * (box_length - 58)
        cPrint(u" ┌────┬" + bars + u"┐",self.color_code[self.info_type])
        cPrint(u" │"+ self.label_code[self.info_type] +u"│" + info + spaces + u"│", self.color_code[self.info_type])
        cPrint(u" └────┴" + bars + u"┘",self.color_code[self.info_type])

    def generate_menu(self,options):
        box_length = 60
        text_length = len(options)

    def time_box(self):# 把时间相关的列出来
        cPrint(u" ┌──────────┐ ┌──────────┐ ┌────────┐",self.color_code["default"])
        cPrint(u" │    Current Time    │ │     Start Time     │ │  Elapsed Time  │",self.color_code["default"])
        cPrint(u" │" + self.time_now() + u" │ │" + self.time_now() + u" │ │" + "  ?? Hr ?? min " + u" │",self.color_code["default"])
        cPrint(u" └──────────┘ └──────────┘ └────────┘",self.color_code["default"])

    def project_box(self):
        box_length = 85
        info = self.info
        msg_length = len(info)
        if msg_length + 44 > box_length:
            info = info[0:box_length-39] + "..."
        msg_length = len(info)    
        spaces = "  " * (box_length - msg_length -44)
        bars = "─" * (box_length - 58)
        cPrint(u" ┌─────┬" + bars + u"┐",self.color_code[self.info_type])
        cPrint(u" │  PROJECT │" + info + spaces + u"│", self.color_code[self.info_type])
        cPrint(u" ├─────┼" + bars + u"┐",self.color_code[self.info_type])
        cPrint(u" │          │" + info + spaces + u"│", self.color_code[self.info_type])
        cPrint(u" │ KEY WORDS│" + info + spaces + u"│", self.color_code[self.info_type])
        cPrint(u" │          │" + info + spaces + u"│", self.color_code[self.info_type])
        cPrint(u" └─────┴" + bars + u"┘",self.color_code[self.info_type])

    def project_menu(self):
        cPrint(u" ┌──────────┐",self.color_code["default"])
        cPrint(u" │ 1.Add New Project  │",self.color_code["default"])
        cPrint(u" │ 2.Edit Project     │",self.color_code["default"])
        cPrint(u" │ 3.Delete Project   │",self.color_code["default"])
        cPrint(u" │ 4.Run Projects     │",self.color_code["default"])
        cPrint(u" └──────────┘",self.color_code["default"])
        while True:
            project_menu_choice = raw_input(u'  >>>  ')
            if project_menu_choice in ["1","2","3","4"]:
                return project_menu_choice
                break
            else:
                print "  Invalid choice, please select again"
                continue



    def time_now(self): # 输出时间
        ISOTIMEFORMAT = '%Y-%m-%d %X' #设定了时间格式
        return time.strftime(ISOTIMEFORMAT, time.localtime())
        

if __name__ == '__main__':
    os.system('cls')
    dis = Output("test of message, hello world,here is more, more and more","safe")
    dis.time_box()
    dis.project_menu()