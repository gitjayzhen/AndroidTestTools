# -*- coding=utf8 -*-
from gui_controller.packageController import PackageController
from gui_controller.apkController import ApkController
from gui_controller.deviceInfo import DeviceInfo
import easygui
import re
import time
import wx
'''
在导入模块的时候，一定要注意在文件夹同级或子集目录下都要有__init__.py文件
业务逻辑:1.首先是确认使用哪一个设备
         2.在该设备上安装哪一个apk
         3.确认完后，进行安装
'''

class ApkInstallGui(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Python Application for Android',pos=(400,100),size=(630,460))
        panel = wx.Panel(self,-1)
        #第一步:确认使用哪一个设备
        self.dinfoObj = DeviceInfo()
        self.deviceInfo = self.dinfoObj.get_devices_as_dict()
        self.device_info_list = self.dinfoObj.get_devices_as_list()
        self.choise_device_res_obj = wx.CheckListBox(panel,-1,(30,20),(480,150),self.device_info_list)
        self.refresh_device_btn = wx.Button(panel,wx.ID_REFRESH,'刷新设备'.decode("utf8"),pos=(520,138),size=(70,32))

        #第二部：在该设备上安装哪一个apk
        self.apkObj = ApkController()
        apk_list = self.apkObj.apk_list()
        self.choise_apk_res_obj = wx.RadioBox(panel,-1,"Apk list",(30,190),(480,210),apk_list,1,wx.RA_SPECIFY_COLS)
        wx.Button(panel,-1,'刷新列表'.decode("utf8"),pos=(520,248),size=(70,32))
        wx.Button(panel,-1,'下载最新'.decode("utf8"),pos=(520,288),size=(70,32))
        self.delete_choise_btn = wx.Button(panel,-1,'删除选中'.decode("utf8"),pos=(520,328),size=(70,32))
        self.button = wx.Button(panel,-1,'立即安装'.decode("utf8"),pos=(520,368),size=(70,32))

        self.Bind(wx.EVT_BUTTON,self.delete_choise,self.delete_choise_btn)
        self.Bind(wx.EVT_BUTTON,self.refresh_device,self.refresh_device_btn)
        self.Bind(wx.EVT_BUTTON,self.on_btn_click,self.button)
    def delete_choise(self,event):
        choise_apk_res = self.choise_apk_res_obj.GetStringSelection()
        apkPath = self.apkObj.apk_abs_path(choise_apk_res)
        b = self.apkObj.delete_apk(apkPath)
        if b:
            wx.MessageBox(apkPath,'delete apk SUCCESSED',wx.OK|wx.ICON_INFORMATION)

    def refresh_device(self,event):
        self.device_info_list = self.dinfoObj.get_devices_as_list()
        wx.MessageBox(str(self.device_info_list),'Install Result Info',wx.OK|wx.ICON_INFORMATION)

    def on_btn_click(self,event):
        choise_apk_res = self.choise_apk_res_obj.GetStringSelection()
        apkPath = self.apkObj.apk_abs_path(choise_apk_res)
        apkPackageName = self.apkObj.get_apk_package_name(apkPath)
        choise_device_res = self.choise_device_res_obj.GetCheckedStrings()
        #第三部：执行安装工作
        pctrObj = PackageController()
        if choise_device_res is None or len(choise_device_res) == 0:
            print "all devices will be installed apk"
            pctrObj.install_all_devices(apkPath,apkPackageName)  #向所有链接的设备安装
        elif choise_device_res[0] == 'All' :
            print "all devices will be installed apk"
            pctrObj.install_all_devices(apkPath,apkPackageName)  #向所有链接的设备安装
        else:
            print "Will install apk on your choise device"
            for i in self.deviceInfo:
                for y in range(len(choise_device_res)):
                    if re.search(self.deviceInfo[i]["phone_model"],choise_device_res[y]):
                        pctrObj.install_one_device(i,apkPath,apkPackageName)
        #wx.MessageBox('Install work is Successed','Install Result Info',wx.OK|wx.ICON_INFORMATION)
        print ">>> Install work is Successed"
if __name__ == '__main__':
    app = wx.App()
    ApkInstallGui().Show()
    app.MainLoop()
