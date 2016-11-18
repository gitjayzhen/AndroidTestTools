#coding=utf-8
from gui_event.gui_events import EventController
import easygui
import re
import time
import wx
'''
以dialog为window窗口展示界面（依然是继承wx.app）：
1.main_vbox为整个窗口界面的垂直分布。
2.显示在最顶层的是vbox1_phone_info，是垂直分布，它的内容是lc_device_info.
3.显示在中间部分是vbox2_apk_info，是垂直分布，其中是lc_apk_info.
4.显示在最下面的是vbox_button，是垂直分布，添加有panel，panel中添加grid_button
'''
class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, pos=(500,150),size=(630, 500),style=wx.DEFAULT_DIALOG_STYLE)
        self.event_ctrl = EventController(self)

        main_vbox = wx.BoxSizer(wx.VERTICAL)#主界面

        vbox1_phone_info = wx.BoxSizer(wx.VERTICAL)
        vbox2_apk_info = wx.BoxSizer(wx.VERTICAL)
        vbox3_button = wx.BoxSizer(wx.VERTICAL)
        grid_button= wx.GridSizer(3,6,5,5)

        #window的上半部分：vbox2（lc_device_info）
        self.lc_device_info = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc_device_info.InsertColumn(0, '品 牌'.decode('utf8'),wx.LIST_FORMAT_RIGHT,width= 80)
        self.lc_device_info.InsertColumn(1, '型 号'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=85)
        self.lc_device_info.InsertColumn(2, '系统版本'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=80)
        self.lc_device_info.InsertColumn(3, '像素密度'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=80)
        self.lc_device_info.InsertColumn(4, '分辨率'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=100)
        self.lc_device_info.InsertColumn(5, 'IP'.decode('utf8'),wx.LIST_FORMAT_CENTER,width=160)
        vbox1_phone_info.Add(self.lc_device_info, 1, wx.EXPAND | wx.ALL, 3)
        self.event_ctrl.refresh_device_info()
        #中间部分显示apk文件目录
        self.lc_apk_info = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
        vbox2_apk_info.Add(self.lc_apk_info, 1, wx.EXPAND | wx.ALL, 3)
        self.event_ctrl.refresh_apk_info()
        #最下面部分显示按钮
        panl = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        vbox3_button.Add(panl, 1, wx.EXPAND | wx.ALL, 3)
        grid_button.AddMany([
                       (wx.Button(panl, 10, '刷新列表'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 11, '清空列表'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 12, '下载最新'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 13, '移除本地'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 14, '截取屏幕'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 15, '重启设备'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 16, '单个安装'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 17, '全部安装'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 18, '覆盖安装'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 19, '清除数据'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 20, '发送数据'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 21, '关闭窗口'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 22, '崩溃日志'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 23, '当前包名'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 24, '当前活动'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 25, '应用权限'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 26, 'CPU消耗'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 27, 'kill 5037'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
])
        panl.SetSizer(grid_button)
        #为各个btn设置时间监听
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_refresh, id=10)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_download, id=12)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_Clear, id=11)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.remove_local_file, id=13)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_capture_window, id=14)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_reboot, id=15)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install, id=16)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install_all, id=17)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_cover_install, id=18)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_clear_data, id=19)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_input_text, id=20)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.on_close, id=21)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_app_crash_log,id=22)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_current_app_package_name,id=23)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_current_app_activity,id=24)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.reset_service_port, id=27)
        #将vbox2和hbox1添加到w_vbox中
        main_vbox.Add(vbox1_phone_info, 1, wx.EXPAND)
        main_vbox.Add(vbox2_apk_info, 1, wx.EXPAND)
        main_vbox.Add(vbox3_button, 1, wx.EXPAND)
        self.SetSizer(main_vbox)

class MyApp(wx.App):
    def OnInit(self):
        dlg = MyDialog(None, -1, '安卓手机辅助工具'.decode("utf8"))
        dlg.ShowModal()
        dlg.Destroy()
        return True

app = MyApp()
app.MainLoop()
