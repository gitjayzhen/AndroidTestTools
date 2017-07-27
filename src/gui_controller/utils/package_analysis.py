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
import os
import re

import wx

from src.gui_controller.core.adb_utils import AndroidUtils
from src.gui_controller.info.device_info import DeviceInfo

'''
主要处理安装和卸载手机上的应用
'''


class PackageController(object):
    def __init__(self):
        self.sno_list = DeviceInfo().get_devices()
        self.android = AndroidUtils()
    '''
    uninstall_All参数指定要卸载的包名，该方法会调用uninstall_One卸载所有链接在电脑上的手机中的应用
    '''
    def uninstall_all(self, package_name):
        devices = self.sno_list
        if devices is None:
            wx.LogMessage("No device is connected")
        else:
            for sno in devices:
                self.uninstall_one(sno, package_name)
    '''
    指定设备，并指定包名进行应用的卸载
    '''
    def uninstall_one(self, sno, package_name):
        uninstall_result = self.android.adb(sno,'uninstall %s'%package_name).stdout.read()
        if re.findall(r'Success',uninstall_result):
            wx.LogMessage('[%s] uninstall [%s] [SUCCESS]' %(sno,package_name))
        else:
            wx.LogMessage('no assign package')
    '''
    apk_name为apk的绝对路径，该方法会调用install_OneDevice方法，向所有设备安装该应用
    '''
    def install_all_devices(self, apk_name, apk_package_name):
        wx.LogMessage("Install all devices")
        device_list = self.sno_list
        if device_list is None:
            wx.LogMessage("No device is connected")
        else:
            for sno in device_list:
                self.install_one_device(sno, apk_name, apk_package_name)

    '''
    指定设备名，并指定apk进行安装，安装前会检测手机是否已经安装了该应用，如果有，先卸载
    '''
    def install_one_device(self, sno, apk_name, apk_package_name):
        had_package = self.android.shell(sno, 'pm list packages |findstr "%s"' % apk_package_name).stdout.read()
        if re.search(apk_package_name, had_package):
            self.uninstall_one(sno, apk_package_name)
        install_result = self.android.adb(sno, 'install %s'%apk_name).stdout.read()
        boolean = self.is_has_package(sno, apk_package_name)
        if re.findall(r'Success', install_result) or boolean:
            wx.LogMessage('[%s] adb install %s [SUCCESS]' % (sno, os.path.basename(apk_name)))
        else:
            wx.LogMessage('[%s] install %s [FALSE]' % (sno, os.path.basename(apk_name)))

    def cover_install(self, sno, apk_name, apk_package_name):
        install_result = self.android.adb(sno, 'install -r %s'%apk_name).stdout.read()
        boolean = self.is_has_package(sno, apk_package_name)
        if re.findall(r'Success', install_result) or boolean:
            wx.LogMessage('[%s] adb install %s [SUCCESS]' % (sno, os.path.basename(apk_name)))
        else:
            wx.LogMessage('[%s] install %s [FALSE]' % (sno, os.path.basename(apk_name)))

    def is_has_package(self, sno, package_name):
        had_package = self.android.shell(sno, 'pm list packages |findstr "%s"'%package_name).stdout.read()
        if re.search(package_name, had_package):
            return True
        else:
            return False

    def clear_app_data(self, sno, package_name):
        b = self.is_has_package(sno, package_name)
        if b:
            res = self.android.shell(sno, "pm clear %s" % package_name).stdout.read()
            if re.search(r'Success', res):
                wx.LogMessage("Clear data Success with [%s]" % package_name)
            else:
                wx.LogMessage("Clear work ERROR")
        else:
            wx.LogMessage("NO Package :", package_name)


