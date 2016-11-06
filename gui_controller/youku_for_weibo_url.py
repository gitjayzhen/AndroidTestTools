# -*- coding:utf-8 -*-
import urllib2
import cookielib
import json
from datetime import datetime
class RequestData():
    def __init__(self):
        pass
    def do_get(self,url_text):
        request_header = {
        'Host':'',
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cookie':'__ysuid=1473417512712xXb; ypvid=14743795374386AFUt5; yseid=14743795374382xarz1; ysestep=1; yseidcount=1; yseidtimeout=1474386737439; ycid=0; ystep=1; juid=01at3tsn132jba; seid=01at3tsn142k1i; referhost=https%3A%2F%2Fwww.google.com.hk; seidtimeout=1474381337444; ykss=fa3ee157011bf65f1307ef9b; cna=tLc4EDfpvTwCAXzKqr6XWdof'
        }

        request_url = "%s"%url_text
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        resp = urllib2.urlopen(request_url)
        a = resp.read()
        json_a = json.loads(a)
        b = json_a["post_links"]["open_scheme"]
        return b



