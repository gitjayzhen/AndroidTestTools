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
# TODO(jayzhen) 这个自定义的exception可有可无，反正没用到
class SriptException(Exception):
    def __init__(self, str):
        self.str = str

    def _str_(self):
        return self.str
