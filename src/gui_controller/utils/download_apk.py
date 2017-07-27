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

from bs4 import BeautifulSoup
import re
import wx
import urllib2
import urllib
import requests
import requests.exceptions
import os


class DownloadApk(object):
    """
    访问指定url的网页，并将网页的内容下载下来
    """
    def download_html(self, url):
        if url is None:
            return None
        try:
            response = urllib2.urlopen(url)    # 访问传送过来的url
        except urllib2.URLError, e:
            wx.LogMessage("URLError >>> NO NETWORKS FOUND")
            return None
        if response.getcode() != 200:      # 如果访问的状态不是：200（成功），返回none
            return None
        content = response.read()
        response.close()
        return content

    def use_requests_download_html(self, url):
        if url is None:
            return None
        try:
            response = requests.get(url)    # 访问传送过来的url
        except requests.exceptions, e:
            wx.LogMessage("URLError >>> NO NETWORKS FOUND")
            return None
        if response.status_code != 200:      # 如果访问的状态不是：200（成功），返回none
            return None
        content = response.text
        response.close()
        return content
    '''
    解析并获取网页中的以apk结尾的链接
    '''
    def get_apk_link_urls(self, htmlcontent):
        try:
            # htmlcontent = self.download_html(web_url)
            soup = BeautifulSoup(htmlcontent, 'html.parser',from_encoding='utf-8')
            apk_urls = []
            apk_times = []
            urls = soup.find_all('a', href=re.compile(r'.*?\.apk'))
            for link in urls:
                new_url = link['href']
                # print new_url
                apk_time = link.parent.next_sibling.string.strip()
                apk_urls.append(new_url)
                apk_time = apk_time.replace(" ", "_").replace(":", "-")
                apk_times.append(apk_time)
            return apk_urls, apk_times
        except TypeError, e:
            wx.LogMessage("TypeError >>> get apk link url happen ERROR")
            return None
    '''
    下载时给出时间信息
    '''
    def get_apk_dict_link_urls(self, htmlcontent):
        try:
            soup = BeautifulSoup(htmlcontent, 'html.parser', from_encoding='utf-8')
            apk_urls = {}
            urls = soup.find_all('a',href=re.compile(r'.*?\.apk'))
            for link in urls:
                apk_url = link['href']
                apk_create_time = link.parent.next_sibling.string
                apk_urls[apk_url] = apk_create_time
            return apk_urls
        except TypeError, e:
            wx.LogMessage("TypeError >>> get apk link url happen ERROR")
            return None
    '''
    在所有的apk链接中以获取最新的一个
    '''
    def get_latest_apk_link(self,urls):
        # dict_info = {}
        dict_big = {}
        for url in urls:
            try:
                url_split_list = url.split('/')[-1].split('_')
                apk_version = url_split_list[2]
                apk_day = url_split_list[3]
                if re.search(r"baidu", apk_day):
                    dict_big["99999"] = url
                    continue
                apk_version_number = url_split_list[4]
                # dict_info[url] = {"version":apk_version,"day":apk_day,"version_number":apk_version_number}
                dict_big[apk_version_number] = url
            except Exception, e:
                continue
        num = max(map(int, dict_big.keys()))
        return dict_big[str(num)]
    '''
    把最新的apk下载下来
    '''
    def output_apk(self, url, apk_time):
        # apath = os.getcwd()
        apath = "C:\\"
        abs_path = os.path.join(apath, "apks")
        if not os.path.exists(abs_path):
            os.mkdir(abs_path)
        apk_file_name = url.split('/')[-1][:-4]
        apk_file_name ="%s_%s.%s"%(apk_file_name, apk_time, "apk")
        path_apk = os.path.join(abs_path, apk_file_name)
        if os.path.exists(path_apk):
            wx.LogMessage("the [%s] is existing" % apk_file_name)
        else:
            wx.LogMessage("download ", url)
            # 添加show dialog的方式，来提示
            urllib.urlretrieve(url, path_apk)
            if os.path.exists(path_apk):
                wx.LogMessage("download completed")

    def get_android_branch_verisons(self, android_url):
        versions_content = self.download_html(android_url)
        try:
            soup = BeautifulSoup(versions_content, 'html.parser', from_encoding='utf-8')
            versions = []
            urls = soup.find_all('a', href=re.compile(r'.*?/$'))
            for link in urls:
                new_url = link['href']
                versions.append(new_url)
            del versions[0]
            return versions
        except TypeError, e:
            wx.LogMessage("TypeError >>> get apk link url happen ERROR")
            return None


