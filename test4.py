# -*- coding: utf-8 -*-
# !/usr/bin/env python

################################################
# Task Name: 三级菜单                           #
# Description：打印省、市、县三级菜单             #
#              可返回上一级                      #
#               可随时退出程序                   #
#----------------------------------------------#
# Author：Oliver Lee                           #
################################################

import ctypes
import sys
reload(sys)
sys.setdefaultencoding('utf8')

zone = {
    'test' : {
        '青岛' : ['四方','黄岛','崂山','李沧','城阳'],
        '济南' : ['历城','槐荫','高新','长青','章丘'],
        '烟台' : ['龙口','莱山','牟平','蓬莱','招远']
    },
    '江苏' : {
        '苏州' : ['沧浪','相城','平江','吴中','昆山'],
        '南京' : ['白下','秦淮','浦口','栖霞','江宁'],
        '无锡' : ['崇安','南长','北塘','锡山','江阴']
    },
    '浙江' : {
        '杭州' : ['西湖','江干','下城','上城','滨江'],
        '宁波' : ['海曙','江东','江北','镇海','余姚'],
        '温州' : ['鹿城','龙湾','乐清','瑞安','永嘉']
    },
    '安徽' : {
        '合肥' : ['蜀山','庐阳','包河','经开','新站'],
        '芜湖' : ['镜湖','鸠江','无为','三山','南陵'],
        '蚌埠' : ['蚌山','龙子湖','淮上','怀远','固镇']
    },
    '广东' : {
        '深圳' : ['罗湖','福田','南山','宝安','布吉'],
        '广州' : ['天河','珠海','越秀','白云','黄埔'],
        '东莞' : ['莞城','长安','虎门','万江','大朗']
    }
}

# def cPrint(info,color): #实现彩色打印  
#     ctypes.windll.Kernel32.GetStdHandle.restype = ctypes.c_ulong  
#     h = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))  
#     if isinstance(color, int) == False or color < 0 or color > 15:  
#         color = Color.default #  
#     ctypes.windll.Kernel32.SetConsoleTextAttribute(h, color)  
#     print info
#     ctypes.windll.Kernel32.SetConsoleTextAttribute(h, Color.form) # 自动回复到银色


province_list = list(zone.keys())             #省列表
# flag = False
# flag1 = False
while True:
    print(u" 省 ".center(50,'*'))
    for i in province_list:
        print(province_list.index(i)+1,i)       #打印省列表
    pro_id = input(u"请输入省编号,或输入q(quit)退出：")   #省ID
    if pro_id.isdigit():
        pro_id = int(pro_id)
        if pro_id > 0 and pro_id <= len(province_list):
            pro_name = province_list[pro_id-1]     #根据省ID获取省名称
            city_list = list(zone[pro_name].keys())    #根据省名称获取对应的值，从新字典中获取key，即市列表
            while True:
                print(u" 市 ".center(50,'*'))
                for v in city_list:
                    print(city_list.index(v)+1,v)       #打印市列表
                city_id = input(u"请输入市编号,或输入b(back)返回上级菜单，或输入q(quit)退出：")
                if city_id.isdigit():
                    city_id = int(city_id)
                    if city_id > 0 and city_id <= len(city_list):
                        city_name = city_list[city_id-1]    #根据市ID获取市名称
                        town_list = zone[pro_name][city_name]   #根据省名称获取对应的值，从新字典中获取值，即县列表
                        while True:
                            print(" 县 ".center(50,'*'))
                            for j in town_list:
                                print(town_list.index(j)+1,j)
                            back_or_quit = input(u"输入b(back)返回上级菜单，或输入q(quit)退出：")
                            if back_or_quit == 'b':
                                break                #终止此层while循环，跳转到上一层While。
                            elif back_or_quit == 'q':
                               # flag1 = True
                               # break               #根据标志位结束程序。
                                exit()
                            else:
                                print(u"输入非法！")
                    else:
                        print(u"编号%d不存在。"%city_id)
                elif city_id == 'b':
                    break
                elif city_id == 'q':
                    # flag = True
                    # break
                    exit()
                else:
                    print(u"输入非法!")
                # if flag1:
                #     break
        else:
            print(u"编号%d不存在。"%pro_id)
    elif pro_id == 'q':
        break
    else:
        print(u"输入非法!")
    # if flag or flag1:
    #     break