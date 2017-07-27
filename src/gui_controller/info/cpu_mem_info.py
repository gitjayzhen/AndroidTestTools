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

# 需要安装pychartdir模块
import wx
from pychartdir import *

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
        if times is None or time == "":
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

    # TODO(jayzhen) 优化抽离成一个特定类
    # 绘制线性图表，具体接口的用法查看ChartDirecto的帮助文档
    def line_chart(self, data):
        wx.LogMessage("Start with the phone performance data to generate a report")
        PATH = lambda p: os.path.abspath(p)
        cpu_data = []
        mem_data = []
        # 去掉cpu占用率中的百分号，并转换为int型
        for cpu in data[0]:
            cpu_data.append(string.atoi(cpu.split("%")[0]))
        # 去掉内存占用中的单位K，并转换为int型，以M为单位
        for mem in data[1]:
            mem_data.append(string.atof(mem.split("K")[0])/1024)
        # 将包名当做图的title，将时间当做x轴的长度
        title = data[2]
        x_limit = data[3]

        # 横坐标
        labels = []
        for i in range(1, x_limit + 1):
            labels.append(str(i))

        # 自动设置图表区域宽度
        if x_limit <= 50:
            xArea = x_limit * 40
        elif 50 < x_limit <= 90:
            xArea = x_limit * 20
        else:
            xArea = 1800

        c = XYChart(xArea, 800, 0xCCEEFF, 0x000000, 1)
        c.setPlotArea(60, 100, xArea - 100, 650)
        c.addLegend(50, 30, 0, "arialbd.ttf", 15).setBackground(Transparent)

        c.addTitle("cpu and memery info (%s)" % title, "timesbi.ttf", 15).setBackground(0xCCEEFF, 0x000000, glassEffect())
        c.yAxis().setTitle("The numerical", "arialbd.ttf", 12)
        c.xAxis().setTitle("Times", "arialbd.ttf", 12)

        c.xAxis().setLabels(labels)

        # 自动设置X轴步长
        if x_limit <= 50:
            step = 1
        else:
            step = x_limit / 50 + 1
        c.xAxis().setLabelStep(step)

        layer = c.addLineLayer()
        layer.setLineWidth(2)
        layer.addDataSet(cpu_data, 0xff0000, "cpu(%)")
        layer.addDataSet(mem_data, 0x008800, "mem(M)")

        path = PATH("%s/logs" % os.getcwd())
        if not os.path.isdir(path):
            os.makedirs(path)

        # 图片保存至脚本当前目录的chart目录下
        c.makeChart(PATH("%s/%s.png" % (path, self.utils.timestamp())))
        wx.LogMessage("End of generating report, cheak file in %s" % path)

