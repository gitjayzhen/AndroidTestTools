# -*- coding=utf-8 -*-
from gui_controller.downloadApk import DownloadApk
import time
downobj = DownloadApk()
forgeturl = ''
urls = downobj.get_apk_link_urls(forgeturl)
url = forgeturl+urls[0]
print "url >>> ",url
downobj.output_apk(url)
time.sleep(4)
