# -*- coding=utf-8 -*-
from gui_controller.downloadApk import DownloadApk
import time
downobj = DownloadApk()
forgeturl = 'http://10.10.152.200/youku/android/V5.8/'
urls = downobj.get_apk_link_urls(forgeturl)
url = forgeturl+urls[0]
print "url >>> ",url
downobj.output_apk(url)
time.sleep(4)
