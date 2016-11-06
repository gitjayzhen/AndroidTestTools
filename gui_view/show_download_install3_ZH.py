#coding=utf-8
from gui_event.gui_events import EventController
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
        self.event_ctrl = EventController(self)
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
        self.event_ctrl.refresh_device_info()

        #window的下半部分：hbox{pnl1[vbox3(lc_apk_info)],pnl2[buttons]}
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        hbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        hbox1.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)

        #vbox3中添加lc2
        self.lc_apk_info = wx.ListCtrl(pnl1, -1, style=wx.LC_LIST|wx.LC_SORT_ASCENDING)
        vbox3.Add(self.lc_apk_info, 1, wx.EXPAND | wx.ALL, 3)
        pnl1.SetSizer(vbox3)

        self.event_ctrl.refresh_apk_info()

        #vbox4中添加buttons
        vbox4.AddMany([(wx.Button(pnl2, 10, '刷新数据'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 11, '下载最新'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 12, '清空下载'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 13, '删除选中'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 14, '移除本地'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 15, '清空设备'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 16, '单个安装'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 17, '多个安装'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 18, '全部安装'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 19, '清除数据'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 21, '覆盖安装'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER),
                       (wx.Button(pnl2, 20, '关闭窗口'.decode('utf8'),size=(80,40)), 0,wx.ALIGN_CENTER)])
        pnl2.SetSizer(vbox4)

        #为各个btn设置时间监听
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_refresh, id=10)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_download, id=11)
        self.Bind(wx.EVT_BUTTON, lambda event,param=12:self.event_ctrl.OnClear(event,param), id=12)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.OnRemove, id=13)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.remove_local_file, id=14)
        self.Bind(wx.EVT_BUTTON, lambda event,param=15:self.event_ctrl.OnClear(event,param), id=15)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install, id=16)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install_more, id=17)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install_all, id=18)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_clear_data, id=19)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.OnClose, id=20)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.OnClose, id=20)

        #将vbox2和hbox1添加到w_vbox中
        w_vbox.Add(vbox2, 1, wx.EXPAND)
        w_vbox.Add(hbox1, 1, wx.EXPAND)
        self.SetSizer(w_vbox)


class MyApp(wx.App):
    def OnInit(self):
        dlg = MyDialog(None, -1, '安卓手机辅助工具'.decode("utf8"))
        dlg.ShowModal()
        dlg.Destroy()
        return True

app = MyApp()
app.MainLoop()
