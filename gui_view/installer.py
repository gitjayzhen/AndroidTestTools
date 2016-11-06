# -*- coding=utf8 -*-
from gui_controller.packageController import PackageController
from gui_controller.apkController import ApkController
from gui_controller.deviceInfo import DeviceInfo
import easygui
import re,time
'''
在导入模块的时候，一定要注意在文件夹同级或子集目录下都要有__init__.py文件
'''

again = time.time()

'''
业务逻辑
1.首先是确认使用哪一个设备
2.在该设备上安装哪一个apk
3.确认完后，进行安装
'''
#第一步:确认使用哪一个设备
dinfoObj = DeviceInfo()
deviceInfo = dinfoObj.catch_devices_info()
infolist = ["All"]
for i in deviceInfo:
    a = deviceInfo[i]["phone_brand"]
    b = deviceInfo[i]["phone_model"]
    c = deviceInfo[i]["os_version"]
    d = deviceInfo[i]["dpi"]
    e = deviceInfo[i]["image_resolution"]
    f = deviceInfo[i]["ip"]
    t = a+"  ::  "+b+"  ::  "+c+"  ::  "+d+"  ::  "+e+"  ::  "+f
    infolist.append(t)
choise_device_res = easygui.choicebox(msg="you can choise then install", title="choise one ? all?", choices=infolist)

#第二部：在该设备上安装哪一个apk
apkObj = ApkController()
apklist = apkObj.apk_list()
choise_apk_res = easygui.choicebox(msg="you can choise then install", title="choise only one ", choices=apklist)
apkPath = apkObj.apk_abs_path(choise_apk_res)

print apkPath

apkPackageName = apkObj.get_apk_package_name(apkPath)
#第三部：执行安装工作
pctrObj = PackageController()
if choise_device_res == 'All' or choise_device_res is None:
    print "all devices will be installed apk"
    pctrObj.install_all_devices(apkPath,apkPackageName)  #向所有链接的设备安装
else:
    for i in deviceInfo:
        if re.search(deviceInfo[i]["phone_model"],choise_device_res):
            pctrObj.install_one_device(i,apkPath,apkPackageName)
print (time.time() - again)
easygui.buttonbox(msg="Installation tasks is over", title="Youku android testing tools", choices=['OK'])
