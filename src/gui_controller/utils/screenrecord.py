#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: screenrecord.py
@time: 2017/12/17 21:41
需求描述：

输入法产品经常会录制产品小视频在给厂商谈合作时使用
一些安卓app录制工具经常会带产品水印什么的

解决方案：

使用python把adb shell screenrecord 封装成一个小工具
使用moviepy库把视频导出成gif
使用wxFormBuilder 制作的窗口
使用pyInstaller打包成exe
"""

import wx
import wx.xrc
import os
from moviepy.editor import *


class MyFrame1(wx.Frame):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 385,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_button_start = wx.Button( self, wx.ID_ANY, u"开始录制", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        bSizer2.Add( self.m_button_start, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button_stop = wx.Button( self, wx.ID_ANY, u"停止录制", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        bSizer2.Add( self.m_button_stop, 0, wx.EXPAND|wx.ALL, 5 )

        self.m_scrolledWindow2 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow2.SetScrollRate( 5, 5 )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_log = wx.StaticText( self.m_scrolledWindow2, wx.ID_ANY, u"日志输出", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_log.Wrap( -1 )
        bSizer3.Add( self.m_log, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_scrolledWindow2.SetSizer( bSizer3 )
        self.m_scrolledWindow2.Layout()
        bSizer3.Fit( self.m_scrolledWindow2 )
        bSizer2.Add( self.m_scrolledWindow2, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )

        self.m_button_start.Bind(wx.EVT_BUTTON, self.onStart)
        self.m_button_stop.Bind(wx.EVT_BUTTON, self.onStop)
        self.m_button_stop.Disable()
        self.log = u"日志输出窗口"
        self.adbpath = os.getcwd()+"\\adb.exe"
        #print self.adbpath
    def __del__( self ):
        pass
    def onStart(self,event):
        import thread
        thread.start_new_thread(self.record,())
        self.m_button_stop.Enable()
        self.m_button_start.Disable()


    def onStop(self,event):
        import subprocess
        self.p.terminate()
        self.log = self.log+u"已停止录制\n"
        self.m_log.SetLabel(self.log)
        import thread
        thread.start_new_thread(self.copy2PC,())
        self.m_button_stop.Disable()

    def copy2PC(self):
        import time
        import subprocess
        self.log = self.log + u"正在拷贝视频到PC\n"
        self.m_log.SetLabel(self.log)
        time.sleep(3)
        self.p = subprocess.Popen(self.adbpath+" pull /sdcard/"+self.filename+".mp4 "+os.getcwd()+"\\"+self.filename+".mp4", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        strout, strerr = self.p.communicate()
        if strerr.lower().find("kb/s") == -1:
            self.log = self.log + u"拷贝失败\n"
            self.m_log.SetLabel(self.log + strerr +"\n")
            self.m_button_start.Enable()
            return
        self.log = self.log + u"已拷贝到程序目录\n"
        self.m_log.SetLabel(self.log)
        self.log = self.log + u"开始转换为gif\n"
        self.m_log.SetLabel(self.log)
        ###开始转换为gif
        myclip = VideoFileClip(os.getcwd()+"\\"+self.filename+".mp4")
        #print (myclip.fps) # prints for instance '30'
        myclip2 = myclip.subclip(0, int(myclip.end))
        myclip2.write_gif(os.getcwd()+"\\"+self.filename+".gif",fps=12) # the gif will have 12 fps
        self.log = self.log + u"gif转换完毕\n"
        self.m_log.SetLabel(self.log)
        self.m_button_start.Enable()


    def record(self):
        import subprocess
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        self.filename = u"Video_"+now

        cmd = self.adbpath+u" shell screenrecord --bit-rate 10000000 /sdcard/"+self.filename+".mp4"
        self.log = u"开始录制\n文件保存在手机//sdcard/"+self.filename+".mp4\n"

        self.m_log.SetLabel(self.log)
        self.p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        strout, strerr = self.p.communicate()
        if strerr != "":
            self.log = self.log + u"录制时出现错误：\n"+strerr
            self.m_log.SetLabel(self.log)
            self.m_button_start.Enable()
            self.m_button_stop.Disable()



#import gizeh
#import moviepy.editor as mpy




app = wx.App(False)
mylog = MyFrame1(None)
mylog.Show()
app.MainLoop()
