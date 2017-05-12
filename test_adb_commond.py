#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
# res = subprocess.Popen("adb shell ifconfig wlan0 | busybox awk 'NR==2{FS="[ :]+";print $4}'", shell=True).stdout.read()
# print res

# output=`dmesg | grep hda`
# becomes
# p1 = subprocess.Popen(["adb", "shell", "ifconfig", "wlan0"], stdout=subprocess.PIPE)
# p2 = subprocess.Popen(["busybox", "awk", "'NR==2{FS="[ :]+";print $4}'"], stdin=p1.stdout, stdout=subprocess.PIPE)
# p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
# output = p2.communicate()[0]
# print output

res = subprocess.Popen("adb shell ifconfig wlan0", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.readlines()

a = res[1].strip()
b = a.split(" ")[1]
print b.split(":")[1]
