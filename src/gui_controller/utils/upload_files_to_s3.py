#!/usr/bin/env python
#-*- coding=utf-8 -*-
""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@software: PyCharm 
@time: 2017/7/21 17:47 

上传S3服务器的脚本

1.获取最新的3个json文件
2.对这三个文件进行重命名
3.检查S3是否有这三个文件，有则删除，没有就上传本地最新的文件

"""
# TODO(jayzhen) 加一个登录功能 已完成
import os
import json
import re
import sys
import getopt
import requests
from requests import Request, Session

login_headers = {"Host": "minio-dev.houbank.net",
           "Connection": "keep-alive",
           "Content-Length": "119",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
           "Origin": "https://minio-dev.houbank.net",
           "x-amz-date": "20170724T024631Z",
           "Content-Type": "application/json",
           "Accept": "*/*",
           "Referer": "https://minio-dev.houbank.net/minio/login",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"}

headers = {"Host": "minio-dev.houbank.net",
           "Connection": "keep-alive",
           "Content-Length": "119",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
           "Origin": "https://minio-dev.houbank.net",
           "x-amz-date": "20170724T063806Z",
           "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MDA2OTM5OTYsImlhdCI6MTUwMDYwNzU5Niwic3ViIjoiODJINzhMUUhTODJVRU9QNTA1R0EifQ.zf_hsOu0F8GkicJV8jqSHppCK7TTvZkbExUrz6zB5EPRm4lAy7GA_nZ4yLHKJXDoBXTvgobJf5olGvNU7WCoiQ",
           "Content-Type": "application/json",
           "Accept": "*/*",
           "Referer": "https://minio-dev.houbank.net/minio/hs-pdl-repay-file/",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"}

work_path = "/home/las/file/out"
# work_path = os.getcwd()

def file_end_with(*endstring):
    ends = endstring
    def run(s):
        f = map(s.endswith,ends)
        if True in f:
            return s
    return run

def pwd_file_list(abs_path, end_string):
    print "工作目录：{}".format(str(abs_path)).decode("utf-8")
    data = []
    backfunc = file_end_with(end_string)
    file_list = os.listdir(abs_path)
    for i in file_list:
        i_path = os.path.join(abs_path, i)
        if os.path.isfile(i_path) and i.endswith("json"):
            data.append(i)
    return data

def get_latest_files(num):
    file_list = pwd_file_list(work_path, ('.json'))
    if len(file_list) < 3:
        print "新生成的json文件不够3个,请检查.".decode("utf-8")
        return None
    if file_list is None:
        return None
    print "当前目录下的共{}个json文件：{}.".format(len(file_list),str(file_list)).decode("utf-8")
    # st = file_list.sort(key=lambda fn: os.path.getmtime(os.getcwd()+"\\"+fn) if not os.path.isdir(os.getcwd()+"\\"+fn) else 0)
    st = file_list.sort(key=lambda fn: os.path.getmtime(work_path+"/"+fn) if not os.path.isdir(work_path+"/"+fn) else 0)

    # 如果期望得到的数目大于当前目录下的文件数，将所有文件返回
    if len(file_list) <= num:
        return file_list
    n = len(file_list) - num
    fname = file_list[n:]
    old_fn = file_list[:n]
    try:
        for old in old_fn:
            old_fp = os.path.join(work_path,old)
            if  os.path.isfile(old_fp) and os.path.isabs(old_fp):
                # 这里注释掉了删除文件的方法 lichrm  /home/las/file/out/b_20170721_01.json
                #os.remove(old_fp)
                os.popen("lichrm {}".format(old_fp))
                print "已经删除了文件: {}".format(old).decode("utf8")
    except OSError as e:
        print "error:删除了文件时，出现了错误".format(old).decode("utf8")
        return None
    return fname

def get_specified_file(fnpc):
    file_list = pwd_file_list(work_path, ('.json'))
    reg = re.compile(fnpc)
    sf = []
    for i in file_list:
        if re.search(reg, i):
             sf.append(i)
    return sf

"""
将文件名中的8位数字形式的日期修改为指定时间点
"""
def replace_file_name(name_str,file_list):
    new_file_list= []
    if name_str is None or file_list is None:
        return None
    try:
        for n in range(len(file_list)):
            fnl = file_list[n].split("_")
            fnl[-2] = name_str
            new_name = "_".join(fnl)
            print "新的文件名: {}".format(new_name).decode("utf-8")
            new_name_p = os.path.join(work_path, new_name)
            old_file_p = os.path.join(work_path, file_list[n])
            if os.path.isfile(old_file_p) and os.path.isabs(old_file_p):
                # os.rename(old_file_p, new_name_p)
                os.popen("sudo mv {} {}".format(old_file_p, new_name_p))
                new_file_list.append(new_name)
        print "文件名修改任务已经完成.".decode("utf-8")
    except IndexError as i:
        print "error:修改文件名发送了错误,可能是目录有非格式化的文件名".decode("utf-8")
        return None
    except OSError as e:
        print "error:修改文件名发送了错误".decode("utf-8")
        return None
    return new_file_list

"""
登陆上S3服务器，并将登录结果中的token保存到后续使用的header
"""
def login_in_s3():
    url = ''
    json_data = {"id":1,"jsonrpc":"2.0","params":{"username":"82H78LQHS82UEOP505GA","password":"tlCyN6J3hBAeVxKLUG8hXIri/I8Ij1xh1LRVGkD9"},"method":"Web.Login"}
    s = Session()
    req = Request('POST', url, json=json_data, headers=login_headers)
    prepped = req.prepare()
    resp = s.send(prepped, verify=True)
    status_num = resp.status_code
    print "登录S3系统，接口返回网络状态 : {}".format(status_num)
    s.close()
    if resp.ok:
        login_res = resp.json()
        token = login_res["result"]["token"]
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        return True
    return False

"""
检测S3上是否已经存在的该文件名的文件
"""
def is_file_on_s3(file_name):
    flag = False
    json_data = {"id":1,"jsonrpc":"2.0","params":{"bucketName":"hs-pdl-repay-file","prefix":"","marker":""},"method":"Web.ListObjects"}
    url= ''
    s = Session()
    req = Request('POST', url,json=json_data,headers=headers)
    prepped = req.prepare()
    resp = s.send(prepped, verify=True)
    print "检查S3系统里是否已有文件，接口返回网络状态 : {}".format(resp.status_code).decode("utf-8")
    try:
        res_json = resp.json()
        file_list_dict = res_json["result"]["objects"]
        for obj in file_list_dict:
            if obj["name"] == file_name:
                print "{} file already exist".format(obj["name"]).decode("utf-8")
                flag = True
    except ValueError as ve:
        print "error:查询S3是否有文件，返回结果不是json格式".decode("utf-8")
    s.close()
    return flag

"""
删除S3上指定文件名的文件
"""
def del_file_from_s3(file_name):
    json_data = {"id":1,"jsonrpc":"2.0","params":{"bucketname":"hs-pdl-repay-file","objects":["aaaa.json"]},"method":"Web.RemoveObject"}
    if file_name is None:
        return False
    del_list = json_data["params"]["objects"]
    if len(del_list) >= 1:
        del_list = []
        del_list.append(file_name)
        json_data["params"]["objects"] = del_list
    print "删除S3上的文件，需要发送的json数据 : {}".format(str(json_data)).decode("utf-8")
    url = ''
    s = Session()
    req = Request('POST', url, json=json_data, headers=headers)
    prepped = req.prepare()
    resp = s.send(prepped, verify=True)
    status_num = resp.status_code
    print "删除S3上的文件，接口返回网络状态 : {}".format(status_num).decode("utf-8")
    s.close()
    if resp.ok:
        return True
    return False
"""
将文件上传到S3服务器上
"""
def upload_file_to_s3(file_name):
    url= '/%s' %file_name
    f = open(os.path.join(work_path,file_name))
    json_data = json.dumps(f.read())
    f.close()
    s = Session()
    req = Request('PUT', url,json=json_data, headers=headers)
    prepped = req.prepare()
    resp = s.send(prepped, verify=True)
    print "上传文件到S3系统，接口返回网络状态 : {}".format(resp.status_code).decode("utf-8")
    s.close()
    if resp.ok:
        return True
    return False


if __name__ == '__main__':
    pattern , args = getopt.getopt(sys.argv[1:], "sn:t:r:") #-s send  -n num -t time_str -r replace
    if pattern is None or len(pattern) <= 0:
        sys.exit(0)
    n = 0
    sf = []
    for op, value in pattern:
        if op == "-t":
            if n == 1:
                continue
            reg_param = value
            sf = get_specified_file(reg_param)
            print "指定文件名的文件：{}.".format(str(sf)).decode("utf-8")
            n += 1
        elif op == "-n":
            num = int(value)
            sf = get_latest_files(num)
            print "最新3个文件的文件名：{}.".format(str(sf)).decode("utf-8")
        elif op == "-r":
            param = value
            if len(value) != 8:
                print "请确认你输入的参数是否是8位数字格式的日期,如：20170721.".decode("utf-8")
                sys.exit(0)
            # 没有使用-n 的时候默认使用 3
            if len(sf) == 0:
                sf = get_latest_files(3)
                print "最新3个文件的文件,看看是不是你要的：{}.".format(str(sf)).decode("utf-8")
            new_file_list = replace_file_name(param, sf)
            # 检查最新三个文件是否已经在S3服务器上，存在就删除，否则就上传该文件
            # 先登录上s3
            if new_file_list is None:
                sys.exit(0)
            login_in_s3()
            for f in new_file_list:
                if is_file_on_s3(f):
                    if del_file_from_s3(f):
                        upload_file_to_s3(f)
                        print "上传{}文件到S3服务器成功,请前往查看.".format(str(f)).decode("utf-8")
                else:
                    if upload_file_to_s3(f):
                        print "上传{}文件到S3服务器成功,请前往查看.".format(str(f)).decode("utf-8")

        elif op == "-s" and n ==1:
            for f in sf:
                if is_file_on_s3(f):
                    print del_file_from_s3(f)
                else:
                    upload_file_to_s3("a_20170721_01.json")











