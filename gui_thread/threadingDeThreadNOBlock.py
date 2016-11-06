# -*- coding: UTF-8 -*-

import thread
from gui_event.guiEvents import EventController


class WorkThread():
    def __init__(self,event,threadID, methodName):

        self.event = event
        self.threadID = threadID
        self.methodName = methodName

    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # 创建新线程
        thread.start_new_thread(function, args)



