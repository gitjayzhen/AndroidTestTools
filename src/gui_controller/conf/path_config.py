#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence
@contact: jayzhen_testing@163.com
@site: http://blog.csdn.net/u013948858
@software: PyCharm
@file: path_config.py
@time: 2017/7/28 11:23
"""
"""
配置的文件开头不要加斜杠了，不然在os.path.join的时候会出错
"""
all_path = {
    "pro_name":"ApkInstallTool",   # 项目名称
    "app_permission_file_path":"logs",   # 每个app的系统使用权限，文档备份目录
    "all_permission_file_path":"src\\gui_controller\\core\\permission.json",   # 总得系统权限文档
    "devices_info_file_path":"logs\\android_devices_info.json",    # 备份设备的信息
    "app_performance_result_path":"logs",   # 性能数据生成图片的目录
    "exception_logs_file_path":"logs"  # 崩溃日志目录
}


