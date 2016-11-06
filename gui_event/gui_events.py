#-*- coding=utf-8 -*-
from gui_controller.package_analysis import PackageController
from gui_controller.apk_controller import ApkController
from gui_controller.device_info import DeviceInfo
from gui_controller.download_apk import DownloadApk
from gui_controller.youku_for_weibo_url import RequestData
import easygui
import re
import time
import wx

class EventController():
    def __init__(self,guiobj):
        self.guiobj = guiobj
        self.dinfoObj = DeviceInfo()
        self.deviceInfo = self.dinfoObj.get_devices_as_dict()
        self.apkObj = ApkController()
        self.pctrObj = PackageController()
        self.repObj = RequestData()

    def refresh_device_info(self):
        self.deviceInfo = self.dinfoObj.get_devices_as_dict()
        if self.deviceInfo is not None:
            for d in self.deviceInfo:
                num_items = self.guiobj.lc_device_info.GetItemCount()
                self.guiobj.lc_device_info.InsertStringItem(num_items, self.deviceInfo[d]["phone_brand"],wx.LIST_FORMAT_RIGHT)
                self.guiobj.lc_device_info.SetStringItem(num_items,1, self.deviceInfo[d]["phone_model"],wx.LIST_FORMAT_CENTER)
                self.guiobj.lc_device_info.SetStringItem(num_items,2, self.deviceInfo[d]["os_version"],wx.LIST_FORMAT_CENTER)
                self.guiobj.lc_device_info.SetStringItem(num_items,3, self.deviceInfo[d]["dpi"],wx.LIST_FORMAT_CENTER)
                self.guiobj.lc_device_info.SetStringItem(num_items,4, self.deviceInfo[d]["image_resolution"],wx.LIST_FORMAT_CENTER)
                self.guiobj.lc_device_info.SetStringItem(num_items,5, self.deviceInfo[d]["ip"] ,wx.LIST_FORMAT_CENTER)

    def do_download(self,event):
        downobj = DownloadApk()
        android_url  = ""
        branch_versions = downobj.get_android_branch_verisons(android_url)
        if branch_versions is None or len(branch_versions) <0:
            return
        dlg = wx.SingleChoiceDialog(None,'Wil download latest apk file with you select version','Apk branch version',branch_versions)
        c_res = dlg.ShowModal()
        if c_res == wx.ID_CANCEL:
            dlg.Destroy()
            return
        elif c_res == wx.ID_OK:
            version = dlg.GetStringSelection()
            dlg.Destroy()
        try:
            forgeturl = android_url + version
            forgeturlcontent = downobj.download_html(forgeturl)
            if forgeturlcontent is None:
                return
            #修改添加时间提示
            apk_urls,apk_times = downobj.get_apk_link_urls(forgeturlcontent)
            if apk_urls is None:
                return
            url = forgeturl+apk_urls[0]
            downobj.output_apk(url,apk_times[0])
            self.refresh_apk_info()
        except TypeError,e:
            print "TypeError >>> show gui happend ERROR"

    def refresh_apk_info(self):
        self.apk_list = self.apkObj.apk_list()
        num_items = self.guiobj.lc_apk_info.GetItemCount()
        if self.apk_list is not None:
            if self.guiobj.lc_apk_info.GetItemCount():
                self.guiobj.lc_apk_info.ClearAll()
            for a in self.apk_list:
                self.guiobj.lc_apk_info.InsertStringItem(num_items,a)

    def do_refresh(self, event):
        if self.guiobj.lc_device_info.GetItemCount():
            self.guiobj.lc_device_info.DeleteAllItems()
        self.refresh_device_info()
        self.refresh_apk_info()

    def OnRemove(self, event):
        index = self.guiobj.lc_apk_info.GetFocusedItem()
        self.guiobj.lc_apk_info.DeleteItem(index)

    def remove_local_file(self,event):
        index = self.guiobj.lc_apk_info.GetFocusedItem()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        md = wx.MessageDialog(None, "will delete local file : %s" %filename, caption="Sure ?", style=wx.OK|wx.CANCEL|wx.CENTRE, pos=wx.DefaultPosition).ShowModal()
        if md == 5100:
            self.apkObj.delete_apk(filepath)
            self.refresh_apk_info()

    def on_close(self, event):
        self.guiobj.Close()

    def OnClear(self, event,param):
        if param is None:
            return
        if param == 100:
            self.guiobj.lc_apk_info.DeleteAllItems()
        elif param == 101:
            self.guiobj.lc_device_info.DeleteAllItems()

    def do_Clear(self,event):
        self.guiobj.lc_device_info.DeleteAllItems()
        self.guiobj.lc_apk_info.DeleteAllItems()

    def do_install(self,event):
        #获取要安装apk的绝对路径
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        #获取被安装apk设备的sno号
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        #执行安装
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.pctrObj.install_one_device(sno,filepath,apkPackageName)
                break
                #pctrObj.is_has_package(sno,apkPackageName)

    def do_install_more(self,event):
        #获取要安装apk的绝对路径
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        #获取被安装apk设备的sno号
        first = self.guiobj.lc_device_info.GetFirstSelected()
        while first != -1:
            phonemodel = self.guiobj.lc_device_info.GetItem(first, col=1).GetText()
            #执行安装
            for sno in self.deviceInfo:
                if self.deviceInfo[sno]["phone_model"] == phonemodel:
                    self.pctrObj.install_one_device(sno,filepath,apkPackageName)
                    self.pctrObj.is_has_package(sno,apkPackageName)
            first = self.lc_device_info.GetNextSelected(first)

    def do_install_all(self,event):
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        self.pctrObj.install_all_devices(filepath, apkPackageName)

    def do_cover_install(self,event):
        #获取要安装apk的绝对路径
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        #获取被安装apk设备的sno号
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        #执行安装
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.pctrObj.cover_install(sno,filepath,apkPackageName)
                break
                #pctrObj.is_has_package(sno,apkPackageName)

    def do_clear_data(self,event):
        index = self.guiobj.lc_device_info.GetFirstSelected()
        if index == -1:
            wx.MessageDialog(self.guiobj, 'NO SELECTION DEVICE', style=wx.OK|wx.CANCEL|wx.CENTRE).ShowModal()
            return
        index = self.guiobj.lc_device_info.GetFirstSelected()
        phonemodel = self.guiobj.lc_device_info.GetItem(index, col=1).GetText()
        dlg = wx.SingleChoiceDialog(None,'Package','package name',["com.youku.phone","com.sina.weibo"],style=wx.OK|wx.CANCEL|wx.CENTRE)
        c_res = dlg.ShowModal()
        if c_res == wx.ID_CANCEL:
            dlg.Destroy()
            return
        elif c_res == wx.ID_OK:
            packagename = dlg.GetStringSelection()
            dlg.Destroy()
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.pctrObj.clear_app_data(sno, packagename)
                break

    def do_input_text(self,event):
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            print ">>>No Choice Device"
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        #弹出一个文本框提示输入信息
        # iptxt_obj = wx.TextEntryDialog(None,'in the "http://v.youku.com/" following',caption="Input to send messages to the phone",  style=wx.OK|wx.CANCEL|wx.CENTRE)
        iptxt_obj = wx.TextEntryDialog(None,'in the following',caption="Input to send messages to the phone",  style=wx.OK|wx.CANCEL|wx.CENTRE)
        while 1:
            iptxt_obj.SetValue("")
            res = iptxt_obj.ShowModal()
            if res == wx.ID_OK:
                txt =  iptxt_obj.GetValue().encode("utf-8")
                # open_scheme_url = self.repObj.do_get(txt)
                # print open_scheme_url
                for sno in self.deviceInfo:
                    if self.deviceInfo[sno]["phone_model"] == phonemodel:
                        self.dinfoObj.input_text(sno,txt)
                        break
            elif res == wx.ID_CANCEL:
                iptxt_obj.Destroy()
                break

    def get_device_items_choised_sno(self):
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            print ">>>Device_items No Choice Device"
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                return sno
        return None

    def do_reboot(self,event):
        sno = self.get_device_items_choised_sno()
        self.dinfoObj.reboot_device(sno)

    def do_capture_window(self, event):
        sno = self.get_device_items_choised_sno()
        self.dinfoObj.capture_window(sno)







