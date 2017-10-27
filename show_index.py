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
import wx
from src.gui_event.transpond_events import EventController

"""
以dialog为window窗口展示界面（依然是继承wx.app）：
1.main_vbox为整个窗口界面的垂直分布。
2.显示在最顶层的是vbox1_phone_info，是垂直分布，它的内容是lc_device_info.
3.显示在中间部分是vbox2_apk_info，是垂直分布，其中是lc_apk_info.
4.显示在最下面的是vbox_button，是垂直分布，添加有panel，panel中添加grid_button
"""


class GuiFrame(wx.Frame):
    def __init__(self, parent, id, title):
        # 只有一个关闭按钮，不能改变大小
        wx.Frame.__init__(self, parent, id, title, pos=(70, 80), size=(1260, 570),
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
                          # style=wx.FULLSCREEN_NOSTATUSBAR | wx.DEFAULT_FRAME_STYLE)
        # 窗口的角标
        self.SetIcon(wx.Icon("src\\gui_view\\studio.ico", wx.BITMAP_TYPE_ICO))
        # self.SetIcon(wx.Icon("gui_view\\studio.ico", wx.TaskBarIcon))
        self.event_ctrl = EventController(self)
        # 主界面
        main_vbox = wx.BoxSizer(wx.VERTICAL)

        vbox1_phone_info = wx.BoxSizer(wx.VERTICAL)
        vbox2_apk_info = wx.BoxSizer(wx.VERTICAL)
        vbox3_button = wx.BoxSizer(wx.VERTICAL)
        grid_button = wx.GridSizer(3, 6, 5, 5)

        # window的上半部分：vbox2（lc_device_info）
        self.lc_device_info = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lc_device_info.InsertColumn(0, '品 牌'.decode('utf8'), wx.LIST_FORMAT_RIGHT, width= 78)
        self.lc_device_info.InsertColumn(1, '型 号'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=85)
        self.lc_device_info.InsertColumn(2, '系统版本'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=78)
        self.lc_device_info.InsertColumn(3, '运行内存'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=78)
        self.lc_device_info.InsertColumn(4, '像素密度'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=78)
        self.lc_device_info.InsertColumn(5, '分辨率'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=100)
        self.lc_device_info.InsertColumn(6, 'IP'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=120)
        self.lc_device_info.InsertColumn(7, 'ID'.decode('utf8'), wx.LIST_FORMAT_CENTER, width=120)
        vbox1_phone_info.Add(self.lc_device_info, 1, wx.EXPAND | wx.ALL, 3)
        self.event_ctrl.refresh_device_info()

        # 设置右键菜单
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)
        self.popupmenu = wx.Menu()
        for text in "dump print".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.event_ctrl.on_popup_item_selected, item)
            self.lc_device_info.Bind(wx.EVT_CONTEXT_MENU, self.event_ctrl.show_popUp)

        # 中间部分显示apk文件目录
        self.lc_apk_info = wx.ListCtrl(self, -1, style=wx.LC_LIST | wx.LC_SORT_ASCENDING)
        vbox2_apk_info.Add(self.lc_apk_info, 1, wx.EXPAND | wx.ALL, 4)
        self.event_ctrl.refresh_apk_info()

        # 最下面部分显示按钮
        panl = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        vbox3_button.Add(panl, 1, wx.EXPAND | wx.ALL, 3)
        grid_button.AddMany([
                       (wx.Button(panl, 10, '刷新列表'.decode('utf8'), size=(80,35)) , 0, wx.ALIGN_CENTER),
                       (wx.Button(panl, 11, '清空列表'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 12, '移除本地'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 13, '录制视频'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 14, '截取屏幕'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 15, '重启设备'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 16, '单个安装'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 17, '全部安装'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 18, '覆盖安装'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 19, '清除数据'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 20, '发送文本'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 21, '杀死进程'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 22, '崩溃日志'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 23, '当前包名'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 24, '当前活动'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 25, '应用权限'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 26, '性能消耗'.decode('utf8'), size=(80,35)), 0,wx.ALIGN_CENTER),
                       (wx.Button(panl, 27, 'kill 5037'.decode('utf8'),size=(80,35)), 0,wx.ALIGN_CENTER),
])
        panl.SetSizer(grid_button)
        # 为各个btn设置事件监听
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_refresh, id=10)
        # self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_download, id=12)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_screenrecord_event, id=13)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_Clear, id=11)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.remove_local_file, id=12)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_capture_window, id=14)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_reboot, id=15)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install, id=16)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_install_all, id=17)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_cover_install, id=18)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_clear_data, id=19)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_input_text, id=20)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_kill_process_event, id=21)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_app_crash_log,id=22)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_current_app_package_name, id=23)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_current_app_activity, id=24)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_app_permission_event, id=25)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.get_app_cpu_mem_thread, id=26)
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.reset_service_port, id=27)
        # 将vbox2和hbox1添加到w_vbox中
        main_vbox.Add(vbox1_phone_info, 1, wx.EXPAND)
        main_vbox.Add(vbox2_apk_info, 1, wx.EXPAND)
        main_vbox.Add(vbox3_button, 1, wx.EXPAND)
        # 添加一个boss容器，log容器，boss容纳主界面
        boss_vbox = wx.BoxSizer(wx.HORIZONTAL)
        log_vbox = wx.BoxSizer(wx.VERTICAL)

        self.log_text_ctrl = wx.TextCtrl(self, id=28, style=wx.TE_MULTILINE, size=(500, 570))
        self.Bind(wx.EVT_BUTTON, self.event_ctrl.do_Clear, id=28)
        log_vbox.Add(self.log_text_ctrl, 1, wx.EXPAND | wx.ALL, 3)
        # 将整个gui的日志进行重定向到指定控件里
        wx.Log.SetActiveTarget(wx.LogTextCtrl(self.log_text_ctrl))

        boss_vbox.Add(main_vbox)
        boss_vbox.Add(log_vbox)

        self.SetSizer(boss_vbox)

if __name__ == "__main__":
    app = wx.App()
    s = GuiFrame(None, -1, 'Android Brigade Tools V12.0 By Jayzhen'.decode("utf8"))
    s.Show()
    app.MainLoop()
