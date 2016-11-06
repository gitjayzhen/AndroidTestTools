#coding=utf-8
from gui_controller.packageController import PackageController
from gui_controller.apkController import ApkController
from gui_controller.deviceInfo import DeviceInfo
from gui_controller.downloadApk import DownloadApk
import easygui
import re
import time
import wx
'''
以dialog为window窗口展示界面（依然是继承wx.app）：
1.w_vbox为整个窗口界面的垂直分布。
2.显示在最顶层的是vbox2，是垂直分布，它的内容是lc_device_info.
3.显示在下半部分是hbox1，是水平分布，左边是pnl1，右边是pnl2.
4.pnl1中有vbox3，vbox3是垂直分布，其中是lc_apk_info。
5.pnl2中有vbox4，vbox4是垂直分布，其中有button。
'''
class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, pos=(500,150),size=(600, 500),style=wx.DEFAULT_DIALOG_STYLE)
        w_vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox4 = wx.GridSizer(4,3,0,0)

        #window的上半部分：vbox2（lc_device_info）
        self.lc_device_info = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc_device_info.InsertColumn(0, '品 牌'.decode('utf8'),wx.LIST_FORMAT_RIGHT,width= 80)
        self.lc_device_info.InsertColumn(1, '型 号'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=85)
        self.lc_device_info.InsertColumn(2, '系统版本'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=80)
        self.lc_device_info.InsertColumn(3, '像素密度'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=80)
        self.lc_device_info.InsertColumn(4, '分辨率'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=100)
        self.lc_device_info.InsertColumn(5, 'IP'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=160)
        vbox2.Add(self.lc_device_info, 1, wx.EXPAND | wx.ALL, 3)
        self.refresh_device_info()

        #window的下半部分：hbox{pnl1[vbox3(lc_apk_info)],pnl2[buttons]}
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        hbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        hbox1.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)

        #vbox3中添加lc2
        self.lc_apk_info = wx.ListCtrl(pnl1, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
        vbox3.Add(self.lc_apk_info, 1, wx.EXPAND | wx.ALL, 3)
        pnl1.SetSizer(vbox3)
        self.refresh_apk_info()

        #vbox4中添加buttons
        vbox4.AddMany([(wx.Button(pnl2, 10, 'Refresh'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 11, 'Download'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 12, 'Clear Apks'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 13, 'RM Choise'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 14, 'RM Local'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 15, 'Clear Devs'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 16, 'Install One'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 17, 'Install More'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 18, 'Install ALL'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 19, 'Clear Data'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER)])
        pnl2.SetSizer(vbox4)

        #为各个btn设置时间监听
        self.Bind(wx.EVT_BUTTON, self.do_refresh, id=10)
        self.Bind(wx.EVT_BUTTON, self.do_download, id=11)
        self.Bind(wx.EVT_BUTTON, lambda event,param=12:self.OnClear(event,param), id=12)
        self.Bind(wx.EVT_BUTTON, self.OnRemove, id=13)
        self.Bind(wx.EVT_BUTTON, self.remove_local_file, id=14)
        self.Bind(wx.EVT_BUTTON, lambda event,param=15:self.OnClear(event,param), id=15)
        self.Bind(wx.EVT_BUTTON, self.do_install, id=16)
        self.Bind(wx.EVT_BUTTON, self.do_install_more, id=17)
        self.Bind(wx.EVT_BUTTON, self.do_install_all, id=18)
        self.Bind(wx.EVT_BUTTON, self.do_clear_data, id=19)

        #将vbox2和hbox1添加到w_vbox中
        w_vbox.Add(vbox2, 1, wx.EXPAND)
        w_vbox.Add(hbox1, 1, wx.EXPAND)
        self.SetSizer(w_vbox)
    '''
    刷新链接上电脑的
    '''
    def refresh_device_info(self):
        self.dinfoObj = DeviceInfo()
        self.deviceInfo = self.dinfoObj.get_devices_as_dict()
        if self.deviceInfo is not None:
            for d in self.deviceInfo:
                num_items = self.lc_device_info.GetItemCount()
                self.lc_device_info.InsertStringItem(num_items, self.deviceInfo[d]["phone_brand"],wx.LIST_FORMAT_RIGHT)
                self.lc_device_info.SetStringItem(num_items,1, self.deviceInfo[d]["phone_model"],wx.LIST_FORMAT_CENTER)
                self.lc_device_info.SetStringItem(num_items,2, self.deviceInfo[d]["os_version"],wx.LIST_FORMAT_CENTER)
                self.lc_device_info.SetStringItem(num_items,3, self.deviceInfo[d]["dpi"],wx.LIST_FORMAT_CENTER)
                self.lc_device_info.SetStringItem(num_items,4, self.deviceInfo[d]["image_resolution"],wx.LIST_FORMAT_CENTER)
                self.lc_device_info.SetStringItem(num_items,5, self.deviceInfo[d]["ip"] ,wx.LIST_FORMAT_CENTER)
    def do_download(self,event):
        downobj = DownloadApk()
        android_url  = "http://10.10.152.200/youku/android/"
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
            forgeturl = android_url + version +"/"
            forgeturlcontent = downobj.download_html(forgeturl)
            if forgeturlcontent is None:
                return
            urls = downobj.get_apk_link_urls(forgeturlcontent)
            if urls is None:
                return
            url = forgeturl+urls[0]
            downobj.output_apk(url)
            self.refresh_apk_info()
        except TypeError,e:
            print "TypeError >>> show gui happend ERROR"
    def refresh_apk_info(self):
        self.apkObj = ApkController()
        self.apk_list = self.apkObj.apk_list()
        num_items = self.lc_apk_info.GetItemCount()
        if self.apk_list is not None:
            if self.lc_apk_info.GetItemCount():
                self.lc_apk_info.ClearAll()
            for a in self.apk_list:
                self.lc_apk_info.InsertStringItem(num_items,a)
    def do_refresh(self, event):
        if self.lc_device_info.GetItemCount():
            self.lc_device_info.DeleteAllItems()
        self.refresh_device_info()

        self.refresh_apk_info()
    def OnRemove(self, event):
        index = self.lc_apk_info.GetFocusedItem()
        self.lc_apk_info.DeleteItem(index)
    def remove_local_file(self,event):
        index = self.lc_apk_info.GetFocusedItem()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        md = wx.MessageDialog(self, "will delete local file : %s" %filename, caption="Sure ?", style=wx.OK|wx.CANCEL|wx.CENTRE, pos=wx.DefaultPosition).ShowModal()
        if md == 5100:
            self.apkObj.delete_apk(filepath)
            self.refresh_apk_info()
    def OnClose(self, event):
        self.Close()
    def OnClear(self, event,param):
        if param is None:
            return
        if param == 12:
            self.lc_apk_info.DeleteAllItems()
        elif param == 15:
            self.lc_device_info.DeleteAllItems()
    def do_install(self,event):
        #获取要安装apk的绝对路径
        index = self.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)

        #获取被安装apk设备的sno号
        choiseitemid = self.lc_device_info.GetFocusedItem()
        #first = self.lc_apk_info.GetFirstSelected()
        #print "foucse:",choiseitemid
        #print "first",first
        #while first != -1:
            #first = self.lc_apk_info.GetNextSelected(first)
            #print "next",first
        #print "count",self.lc_apk_info.GetSelectedItemCount()
        if choiseitemid == -1:
            return
        phonemodel = self.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        #执行安装
        pctrObj = PackageController()
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                pctrObj.install_one_device(sno,filepath,apkPackageName)
                #pctrObj.is_has_package(sno,apkPackageName)
    def do_install_more(self,event):
        #获取要安装apk的绝对路径
        index = self.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)

        #获取被安装apk设备的sno号
        pctrObj = PackageController()
        first = self.lc_device_info.GetFirstSelected()
        while first != -1:
            phonemodel = self.lc_device_info.GetItem(first, col=1).GetText()
            #执行安装
            for sno in self.deviceInfo:
                if self.deviceInfo[sno]["phone_model"] == phonemodel:
                    pctrObj.install_one_device(sno,filepath,apkPackageName)
                    pctrObj.is_has_package(sno,apkPackageName)
            first = self.lc_device_info.GetNextSelected(first)
    def do_install_all(self,event):
        #获取要安装apk的绝对路径
        index = self.lc_apk_info.GetFirstSelected()
        filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)

        #获取被安装apk设备的sno号
        pctrObj = PackageController()
        pctrObj.install_all_devices(filepath, apkPackageName)
    def do_clear_data(self,event):
        dlg = wx.SingleChoiceDialog(None,'Package','package name',["com.youku.phone"],style=wx.ID_OK |wx.CENTER)
        c_res = dlg.ShowModal()
        if c_res == wx.ID_CANCEL:
            dlg.Destroy()
            return
        elif c_res == wx.ID_OK:
            packagename = dlg.GetStringSelection()
            dlg.Destroy()
        index = self.lc_device_info.GetFocusedItem()
        phonemodel = self.lc_device_info.GetItem(index, col=1).GetText()
        pctrObj = PackageController()
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                pctrObj.clear_app_data(sno, packagename)
                break


class MyApp(wx.App):
    def OnInit(self):
        dlg = MyDialog(None, -1, 'Show My Android Work On Python Application')
        dlg.ShowModal()
        dlg.Destroy()
        return True

app = MyApp()
app.MainLoop()
