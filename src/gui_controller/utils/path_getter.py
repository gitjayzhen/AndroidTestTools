#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@file: path_getter.py
@time: 2017/7/28 11:35
"""
import os
from src.gui_controller.conf.path_config import all_path

class FilePathGetter(object):
    def __init__(self):
        self.pro_path = os.getcwd() # .split("src")[0]

    """
    20170728 做路径的判断，如果这个路径不存在，但是个绝对路径，那就创建路径
             做文件的判断文件
    """
    def join_path_to_abs(self, relative_path, file_name=None):
        absp = os.path.join(self.pro_path, relative_path)
        # print "path :", absp
        # print "is exists:", os.path.exists(absp)
        # print "is abs path:", os.path.isabs(absp)
        # print "is dir:", os.path.isdir(absp)
        # print "is file :", os.path.isfile(absp)
        if not os.path.exists(absp):
            os.makedirs(absp)
        if file_name is not None and len(file_name.split(".")) > 1:
            absp = os.path.join(absp, file_name)
        if os.path.isabs(absp):
            return os.path.abspath(absp)
        return None

    def get_project_pwd(self):
        return self.join_path_to_abs(all_path["pro_name"])

    def get_app_permission_file_path(self, file_name):
        return self.join_path_to_abs(all_path["app_permission_file_path"], file_name)

    def get_all_permission_file_path(self):
        relative_path =  all_path["all_permission_file_path"]
        return self.join_path_to_abs(relative_path)

    def get_devices_info_file_path(self):
        return self.join_path_to_abs(all_path["devices_info_file_path"])

    def get_app_performance_result_path(self, file_name):
        return self.join_path_to_abs(all_path["app_performance_result_path"], file_name)

    def get_exception_logs_file_path(self, file_name):
        return self.join_path_to_abs(all_path["exception_logs_file_path"], file_name)