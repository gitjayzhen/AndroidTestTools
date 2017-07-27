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

from src.gui_controller.info.cpu_mem_info import AppPerformanceMonitor

# TODO(jayzhen) 需要完善线程机制
class Threads(object):

    def get_performance(self, sno, time1, pkg):
        apm = AppPerformanceMonitor()
        data = apm.top(sno, time1, pkg)
        apm.line_chart(data)
        wx.LogMessage("threading is running? {}".format(self.t.is_alive()))