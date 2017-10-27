#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: jayzhen 
@license: Apache Licence
@file: report_generator.py
@time: 2017/7/28 10:34
"""
# 需要安装pychartdir模块
import wx
import time
from pychartdir import *
from src.gui_controller.utils.path_getter import FilePathGetter

class Reporter(object):
    def __init__(self):
        self.fp = FilePathGetter()
    # (jayzhen) 优化抽离成一个特定类 已完成
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
            mem_data.append(string.atof(mem.split("K")[0]) / 1024)
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

        # 图片保存至脚本当前目录的chart目录下
        time_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        report_path = self.fp.get_app_performance_result_path("%s.png" % time_str)
        c.makeChart(report_path)
        wx.LogMessage("End of generating report, cheak file in %s" % report_path)

