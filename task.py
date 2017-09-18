# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: task.py
   Description: 处理运行任务
   Author: Dexter Chen
   Date：2017-09-16
-------------------------------------------------
   Development Note：
   1. 根据选择，确定程序执行时间（时间表）
   2. 将制定好的时间表，放入csv文件
   3. 按照时间表执行
   4. 监控执行情况，实时统计
   5. 看门狗程序，必要时重启
   6. 记录运行出现的问题
-------------------------------------------------
   Change Log:
   2018-09-16: 
-------------------------------------------------
   格式：
   task = 
-------------------------------------------------
"""
import sys
import os
import thread
from threading import Timer
from datetime import date, datetime, timedelta
import project as pr
import data_handler as dh
import utilities as ut

reload(sys)
sys.setdefaultencoding('utf8')

task = []

class Watchdog:  # 看门狗程序，防止运行卡死
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
        cPrint(u'\n ●调 等待太久，程序强制跳过 \n', COLOR.RED)
        self.StopWatchdog()
        thread.interrupt_main()
        return

    def StopWatchdog(self):
        ''' Stops the watchdog timer. '''
        self._timer.cancel()

def run_task(startTime, loopTime):  # 多少时间后开始运行
    global currentTime, endTime, timeElapse  # 结束时间是全局的
    currentTime = datetime.now()  # 刷新一下时间
    nowTime = ut.time_str()
    period = timedelta(seconds = loopTime)  # 定义循环间隔
    if startTime == "":  # 开始时间
        strStartTime = strNowTime
    else:
        strStartTime = startTime
    runPeriod = timedelta(hours = runTime)
    endTime = currentTime + runPeriod

    niuniu = Watchdog()  # 生成看门狗

    while True:  # 开始循环
        currentTime = datetime.now()
        strCurrentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')
        timeElapse = currentTime - nowTime
        if str(strCurrentTime) > str(strStartTime):  # 只要超过，就运行，不等于，因为往往运行滞后。此步骤增强稳定性
            niuniu.StartWatchdog()  # 开始看门狗
            Tasks()
            nextTime = currentTime + period
            strStartTime = nextTime.strftime('%Y-%m-%d %H:%M:%S')
            niuniu.StopWatchdog()  # 喂看门狗
            continue

def generate_task_list(project_name_list, delay, minimal_interval): # 
    for project_name in project_name_list:
        key_words = dh.text_read(dh.file_name(project_name),"key_words")






if __name__ == '__main__':
    print project_read()
    # print project_name()
