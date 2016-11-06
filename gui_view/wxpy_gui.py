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

业务逻辑
1.首先是确认使用哪一个设备
2.在该设备上安装哪一个apk
3.确认完后，进行安装
'''


class ApkInstallGui(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Python Application for Android',pos=(400,100),size=(600,550))
        panel = wx.Panel(self,-1)

        #第一步:确认使用哪一个设备
        dinfoObj = DeviceInfo()
        self.deviceInfo = dinfoObj.catch_devices_info()
        self.infolist = ["All"]
        for i in self.deviceInfo:
            a = self.deviceInfo[i]["phone_brand"]
            b = self.deviceInfo[i]["phone_model"]
            c = self.deviceInfo[i]["os_version"]
            d = self.deviceInfo[i]["dpi"]
            e = self.deviceInfo[i]["image_resolution"]
            f = self.deviceInfo[i]["ip"]
            t = a+"  ::  "+b+"  ::  "+c+"  ::  "+d+"  ::  "+e+"  ::  "+f
            self.infolist.append(t)

        self.choise_device_res_obj = wx.CheckListBox(panel,-1,(30,20),(500,100),self.infolist)

        #第二部：在该设备上安装哪一个apk
        self.apkObj = ApkController()
        apklist = self.apkObj.apk_list()

        self.choise_apk_res_obj = wx.RadioBox(panel,-1,"Apk list",(30,140),(500,200),apklist,1,wx.RA_SPECIFY_COLS)

        self.button = wx.Button(panel,-1,'立即安装'.decode("utf8"),pos=(440,400))
        self.Bind(wx.EVT_BUTTON,self.on_btn_click,self.button)

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
        wx.MessageBox('Install work is Successed','Install Result Info',wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    ApkInstallGui().Show()
    app.MainLoop()
