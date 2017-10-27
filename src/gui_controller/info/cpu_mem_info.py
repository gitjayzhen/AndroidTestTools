#!/usr/bin/env python
# -*- encoding: utf-8  -*-

""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@site: http://blog.csdn.net/u013948858 
@software: PyCharm 
@time: 2017/7/27 23:29 
"""
import wx
import string
from src.gui_controller.core.adb_utils import AndroidUtils
from src.gui_controller.info.device_info import DeviceInfo


class AppPerformanceMonitor(object):
    def __init__(self):
        # 打开待测应用，运行脚本，默认times为30次（可自己手动修改次数），获取该应用cpu、memory占用率的曲线图，图表保存至chart目录下
        self.utils = AndroidUtils()

    # 获取cpu、mem占用
    def top(self, sno, times, pkg_name):
        wx.LogMessage("Start getting data on your phone's performance")
        cpu = []
        mem = []
        if times is None or times == "":
            # top次数
            times = 30
        else:
            times = string.atoi(times)
            if times < 15 and times > 0:
                times = 20
        di = DeviceInfo()
        if pkg_name is None or pkg_name == "" or not di.is_installed_package(sno, pkg_name):
            pkg_name = self.utils.get_current_package_name(sno)
        elif di.is_running_package(sno, pkg_name):
            # 设备当前运行应用的包名
            pkg_name = pkg_name
        else:
            return None
        wx.LogMessage("We're going to get the data of [{}] application  ".format(pkg_name))
        top_info = self.utils.shell(sno, "top -n %s | findstr %s$" % (str(times), pkg_name)).stdout.readlines()
    #  PID PR CPU% S #THR VSS RSS PCY UID Name
        for info in top_info:
            # temp_list = del_space(info)
            temp_list = info.split()
            cpu.append(temp_list[2])
            mem.append(temp_list[6])
        wx.LogMessage("The operation of data acquisition of mobile phone performance is completed")
        return cpu, mem, pkg_name, times

