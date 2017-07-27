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

搜集手机某一个应用程序的流量，当前只针对小米手机
"""
from __future__ import division
from src.gui_controller.core.adb_utils import AndroidUtils
# TODO 轮子已经有雏形了，已经完成了基本数据的收集，随后的报表生成逻辑有需求再添加


class FlowPerformanceMonitor(object):

    def __init__(self, sno, pkg):
        self.android = AndroidUtils()
        self.sno = sno
        self.pkg = pkg
        self.pid = self.android.get_app_uid(self.sno, self.pkg)

    def get_app_uid(self):
        self.pid = self.android.get_app_uid(self.sno, self.pkg)

    def __get_tcp_snd(self):
        snd = self.android.shell(self.sno, "cat /proc/uid_stat/%s/tcp_snd" %self.pid).stdout.read()
        # print "Transmit Bytes : {} Bytes".format(snd.strip())
        return int(snd.strip())

    def __get_tcp_rcv(self):
        rcv = self.android.shell(self.sno, "cat /proc/uid_stat/%s/tcp_rcv" % self.pid).stdout.read()
        # r_kb = int(rcv.strip())
        # print "---------------Receive Bytes : {} Bytes".format(rcv.strip())
        return int(rcv.strip())

    def get_tcp_rec_snd(self):
        snd = self.__get_tcp_snd()
        rcv = self.__get_tcp_rcv()
        return rcv, snd

    def get_net_xt_qtaguid(self):
        result = self.android.shell(self.sno, "cat /proc/net/xt_qtaguid/stats | findstr %s | findstr wlan0" % self.pid).stdout.readlines()
        rcv = 0
        snd = 0
        for line in result:
            thread_flow = (line.strip()).split(" ")
            rcv = rcv + int(thread_flow[5])
            snd = snd + int(thread_flow[7])
        return rcv, snd

    def get_tcp_flow(self):
        data = None
        try:
            data = self.get_tcp_rec_snd()
        except ValueError as ve:
            # print ve.message
            data = self.get_net_xt_qtaguid()
        return data

    def get_flow_data(self, times):
        init_flow = self.get_tcp_flow()
        rcv = [0]
        snd = [0]
        for i in range(times):
            flow = self.get_tcp_flow()
            rcv.append((flow[0] - init_flow[0])/1024)
            snd.append((flow[1] - init_flow[1])/1024)
        return rcv, snd

if __name__ == "__main__":
    f = FlowPerformanceMonitor("90d1894b7d62", "com.youku.phone")
    a = f.get_flow_data(50)
    print a[0]
    print a[1]
    # init_a = self.get_tcp_flow()
    # a1 = init_a[0]
    # b1 = init_a[1]
    # print "Transmit :{} Bytes ---- Receive :{} Bytes".format(a1, b1)
    # i = 0
    # for i in times:
    #     flow = self.get_tcp_flow()
    #     a2 = flow[0]
    #     b2 = flow[1]
    #     if i == 49:
    #         print "Transmit :{} Bytes ---- Receive :{} Bytes".format(a2, b2)
    #         a = (a2 - a1) / 1024
    #         b = (b2 - b1) / 1024
    #         print "Total Receive :{}kB , Total Transmit :{}kB".format(a, b)