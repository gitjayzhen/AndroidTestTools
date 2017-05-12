#!/usr/bin/env python
# -*-coding=utf8 -*-
from __future__ import division
import os
import re
import time
from scriptUtils.utils import AndroidUtils


class DeviceInfo():
    def __init__(self):
        self.android = AndroidUtils()
    '''
        获取连接上电脑的手机设备，返回一个设备名的list
    '''
    def get_devices(self):
        sno_list = self.android.get_device_list()
        return sno_list

    '''
    根据不同的需求，设计了返回dict和list格式的两个function。
    '''
    def get_devices_as_dict(self):
        try:
            info = {}
            lists = self.get_devices()
            if not lists or len(lists) <= 0:
                print ">>>NO Device connected"
                return None
            for sno in lists:
                sno,phone_brand,phone_model,os_version,ram,dpi,image_resolution,ip = self.get_info(sno)
                info[sno] = {"phone_brand":phone_brand,"phone_model":phone_model,"ram":ram,"os_version":os_version,"dpi":dpi,"image_resolution":image_resolution,"ip":ip}
            return info
        except TypeError, e:
            return None

    def get_devices_as_list(self):
        info_list = self.get_devices_as_dict()
        devices_as_lsit = ["All"]
        for i in info_list:
            a = info_list[i]["phone_brand"]
            b = info_list[i]["phone_model"]
            c = info_list[i]["os_version"]
            d = info_list[i]["dpi"]
            e = info_list[i]["image_resolution"]
            f = info_list[i]["ip"]
            t = a+"  ::  "+b+"  ::  "+c+"  ::  "+d+"  ::  "+e+"  ::  "+f
            devices_as_lsit.append(t)
        return devices_as_lsit

    '''
    通过adb命令来获取连接上电脑的设备的信息。
    '''
    def get_info(self,sno):
        phone_brand = None
        phone_model = None
        os_version = None
        ram = None
        dpi = None
        image_resolution = None
        ip = None
        try:
            result = self.android.shell(sno, "cat /system/build.prop").stdout.readlines()
            for res in result:
                #系统版本
                if re.search(r"ro\.build\.version\.release",res):
                    os_version = res.split('=')[-1].strip()
                #手机型号
                elif re.search(r"ro\.product\.model",res):
                    phone_model = res.split('=')[-1].strip()
                #手机品牌
                elif re.search(r"ro\.product\.brand",res):
                    phone_brand = res.split('=')[-1].strip()
            ip = self.get_device_wifi_ip(sno)
            image_resolution = self.get_device_distinguishability(sno)
            dpi = self.android.shell(sno, "getprop ro.sf.lcd_density").stdout.read()
            proc_meninfo = self.android.shell(sno, "cat /proc/meminfo").stdout.readline()
            ram = self.get_device_ram(sno)
            return sno, phone_brand, phone_model, os_version, str(ram)+"GB", dpi.strip(), image_resolution, ip.strip()
        except Exception,e:
            print ">>> Get device info happend ERROR :"+ str(e)
            return None

    def input_text(self,sno,text):
        text_list = list(text)
        specific_symbol = set(['&', '@', '#', '$', '^', '*'])
        for i in range(len(text_list)):
            if text_list[i] in specific_symbol:
                if i-1 < 0:
                    text_list.append(text_list[i])
                    text_list[0] = "\\"
                else:
                    text_list[i-1] = text_list[i-1] + "\\"
        seed = ''.join(text_list)
        self.android.shell(sno, 'input text "%s"'%seed)

    def reboot_device(self, sno):
        self.android.adb(sno, "reboot")

    def capture_window(self,sno):
        self.android.shell(sno, "rm /sdcard/screenshot.png").wait()
        self.android.shell(sno, "/system/bin/screencap -p /sdcard/screenshot.png").wait()
        print ">>>截取屏幕成功，在桌面查看文件。"
        c_time = time.strftime("%Y_%m_%d_%H-%M-%S")
        self.android.adb(sno, 'pull /sdcard/screenshot.png T:\\%s.png"'%c_time).wait()

    def get_crash_log(self,sno):
        # 获取app发生crash的时间列表
        time_list = []
        result_list = self.android.shell(sno,"dumpsys dropbox | findstr data_app_crash").stdout.readlines()
        for time in result_list:
            temp_list = time.split(" ")
            temp_time= []
            temp_time.append(temp_list[0])
            temp_time.append(temp_list[1])
            time_list.append(" ".join(temp_time))

        if time_list is None or len(time_list) <=0:
            print ">>>No crash log to get"
            return None
        log_file = "T://Exception_log_%s.txt" %self.android.timestamp()
        f = open(log_file, "wb")
        for time in time_list:
            cash_log = self.android.shell(sno,"dumpsys dropbox --print %s" %time).stdout.read()
            f.write(cash_log)
        f.close()
        print ">>>check local file"

    def current_package_name(self,sno):
        if sno is None or sno == "":
            print ">>>Device_items No Choice Device"
            return
        current_pkg = self.android.get_current_package_name(sno)
        print ">>>package name of current app is [" + current_pkg + "]"
        return current_pkg

    def current_activity(self, sno):
        if sno is None or sno == "":
            print ">>>Device_items No Choice Device"
            return
        print ">>>activity fo current app is [" + self.android.get_current_activity(sno)+"]"

    def win_serivce_port_restart(self):
        self.android.stop_and_restart_5037()

    def screenrecord(self, sno, times):
        self.android.get_srceenrecord(sno, times, "T:\\")

    def do_kill_process(self, sno, package):
        self.android.execute_kill_specified_process(sno,package)

    def do_get_app_permission(self, sno, package_name):
        self.android.get_permission_list(sno, package_name)

    """
    20170512 jayzhen 因为有些手机在getprop中无法获取到ip，那么就使用ifconfig命令，这种情况出现在Android6.0系统以上
    :param sno: 手机的唯一id
    :return: 手机的wifi下的网络ip
    """
    def get_device_wifi_ip(self, sno):
        ip = self.android.shell(sno, "getprop dhcp.wlan0.ipaddress").stdout.read()
        if len(ip) < 5:
            res = self.android.shell(sno, "ifconfig wlan0").stdout.readlines()
            ip = (res[1].strip().split(" ")[1]).split(":")[1]
        return ip

    """
    20170512 jayzhen 调整获取分辨率的方式
    :param sno: 
    :return: image_resolution
    """
    def get_device_distinguishability(self, sno):
        res_4_2 = self.android.shell(sno, "dumpsys window").stdout.read()
        r_4_2 = "init=(\d*x\d*)"
        reg_4_2 = re.compile(r_4_2)
        image_list_4_2 = re.findall(reg_4_2, res_4_2)
        if len(image_list_4_2) > 0:
            image_resolution = image_list_4_2[0]
        else:
            res_4_4 = self.android.shell(sno, "wm size").stdout.read()
            r_4_4 = "Physical size: (\d*x\d*)"
            reg_4_4 = re.compile(r_4_4)
            image_list_4_4 = re.findall(reg_4_4, res_4_4)
            image_resolution = image_list_4_4[0]
            if len(image_list_4_4) < 0:
                image_resolution = "NULL"
        return image_resolution

    """
    20170512 jayzhen 将获取手机运行内存的方式从device_info中隔离出来：使用四舍五入的方式，算的手机的运行内存：int(round(x))或int(2*x)/2+int(2*x)%2
    :param sno: 
    :return: 
    """
    def get_device_ram(self, sno):
        try:
            mem_size = int(proc_meninfo.split(" ")[-2])
            ram = int(round(mem_size / (1024 * 1024)))
            """
            ram = (int(proc_meninfo.split(" ")[-2])//1000000)
            if int(proc_meninfo.split(" ")[-2]) % 1000000 >= 500000:
                ram += 1
            """
            return ram
        except IndexError, e:
            print ">>> Get deivce rom size happend: %s" % str(e)
            ram = "X"
            return ram
