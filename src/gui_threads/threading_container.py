#!/usr/bin/env python  
# -*- encoding: utf-8  -*-

""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@site: http://blog.csdn.net/u013948858 
@software: PyCharm 
@file: threading_container.py 
@time: 2017/7/27 22:47 
"""
import wx
import threading
from src.gui_controller.utils.report_generator import Reporter
from src.gui_controller.info.cpu_mem_info import AppPerformanceMonitor
from src.gui_controller.info.device_info import DeviceInfo
# (jayzhen) 需要完善线程机制   已完成


class GuiThreads(object):
    """
    20170728  搞定了cpu和mem的线程改造
    """
    def __init__(self):
        self.performace_t = None
        self.screenrecord_t = None
        self.dinfoObj = DeviceInfo()

    def run_thread(self, func, args):
        if "performance" == func:
            self.performace_t = threading.Thread(target=self.get_performance, args=args)
            self.performace_t.start()
        elif "screenrecord" == func:
            self.screenrecord_t = threading.Thread(target=self.get_screenrecord, args=args)
            self.screenrecord_t.start()

    def get_performance(self, sno, time1, pkg):
        wx.LogMessage("get preforence func threading process is running: {}".format(self.performace_t.is_alive()))
        apm = AppPerformanceMonitor()
        data = apm.top(sno, time1, pkg)
        reporter = Reporter()
        reporter.line_chart(data)
        wx.LogMessage("threading is running? {}".format(self.performace_t.is_alive()))

    def get_screenrecord(self, sno, times):
        self.dinfoObj.screenrecord(sno, times)
        wx.LogMessage("threading is running? {}".format(self.screenrecord_t.is_alive()))
