#-*-coding=utf8 -*-
import os
import re
import time
'''
ro.build.version.release=4.0.3(android版本
ro.product.model=S2(手机型号)--
ro.product.brand=Spreadtrum(手机品牌)
ro.product.name=sp6825eb_7661plus(手机正式名称)
ro.product.device=sp6825eb_7661（采用的设备）
ro.product.board=sp6825eb_7661（采用的主板）
ro.product.cpu.abi=armeabi-v7a（cpu的版本）
ro.product.cpu.abi2=armeabi(CPU品牌)
ro.product.manufacturer=Spreadtrum(手机制造商)
'''
class DeviceInfo():
    def __init__(self):
        pass
    '''
        获取连接上电脑的手机设备，返回一个设备名的list
    '''
    def get_devices(self):
        device_list = os.popen("adb devices").readlines()
        sno_list = []
        for d in device_list:
            if re.search(r'device$',d):
                sno = d.split('device')[0].strip()
                sno_list.append(sno)
        return sno_list

    '''
    根据不同的需求，设计了返回dict和list格式的两个function。
    '''
    def get_devices_as_dict(self):
        try:
            info = {}
            lists = self.get_devices()
            for sno in lists:
                sno,phone_brand,phone_model,os_version,dpi,image_resolution,ip = self.get_info(sno)
                info[sno] = {"phone_brand":phone_brand,"phone_model":phone_model,"os_version":os_version,"dpi":dpi,"image_resolution":image_resolution,"ip":ip}
            return info
        except TypeError,e:
            return None

    def get_devices_as_list(self):
        info_list = self.get_devices_as_dict()
        devices_as_lsit = ["All"]
        for i in info_list:
            a = info_list[i]["phone_brand"]
            b = info_list[i]["phone_model"]
            c = info_list[i]["os_version"]
            d = info_list[i]["dpi"]
            e = info_list[i]["image_resolution"]
            f = info_list[i]["ip"]
            t = a+"  ::  "+b+"  ::  "+c+"  ::  "+d+"  ::  "+e+"  ::  "+f
            devices_as_lsit.append(t)
        return devices_as_lsit

    '''
    通过adb命令来获取连接上电脑的设备的信息。
    '''
    def get_info(self,sno):
        try:
            result = os.popen("adb -s %s shell cat /system/build.prop"%sno).readlines()
            for res in result:
                #系统版本
                if re.search(r"ro\.build\.version\.release",res):
                    os_version = res.split('=')[-1].strip()
                #手机型号
                elif re.search(r"ro\.product\.model",res):
                    phone_model = res.split('=')[-1].strip()
                #手机品牌
                elif re.search(r"ro\.product\.brand",res):
                    phone_brand = res.split('=')[-1].strip()
            ip = os.popen("adb -s %s shell getprop dhcp.wlan0.ipaddress"%sno).read()
            dpi = os.popen("adb -s %s shell getprop ro.sf.lcd_density"%sno).read()
            res_4_2 = os.popen("adb -s %s shell dumpsys window"%sno).read()
            res_4_4 = os.popen("adb -s %s shell wm size"%sno).read()
            r_4_2 = "init=(\d*x\d*)"
            r_4_4 = "Physical size: (\d*x\d*)"
            reg_4_4 = re.compile(r_4_4)
            reg_4_2 = re.compile(r_4_2)
            image_list_4_4 = re.findall(reg_4_4,res_4_4)
            image_list_4_2 = re.findall(reg_4_2,res_4_2)
            if len(image_list_4_4) > 0:
                image_resolution = image_list_4_4[0]
            elif len(image_list_4_2) > 0:
                image_resolution = image_list_4_2[0]
            else:
                image_resolution = "NULL"
            return sno,phone_brand,phone_model,os_version,dpi,image_resolution,ip
        except Exception,e:
            print ">>> NO Android Device"
            return None
    '''
    输入很长的字符,特殊字符，使用adb shell input 的时候会出问题  例如 特殊字符“&”
    此时有两种方法：
    1.使用转意符,就能正常输入了
      adb shell input text "\&" #该命令执行后，手机文本输入框中就会有“&”
      缺点：每个“&”前都要加一个转意符，否则会报错
      例如： adb shell input text "\&dd&&" ，会报错
    2.加一个空格字符前加一个空格，后面跟多少个特殊字符（&）都无所谓 adb shell input text " &&&&&&&hhd&&"
    综上可以看出，adb shell input text中空格和'\'都是有特殊含义的
    如果想在手机的编辑框中输入一个空格怎么办，这个就不能用 adb shell input text命令了
    直接用 adb shell input  keyevent  62 就好了
    输入'\'这个暂时没有好方法，adb shell input text " \h"  可以直接输入“\h”, 但是没有h，会报错
    如果有好的方法欢迎补充
    这个在输入网址的时候比较有用，尤其是url中的参数
    '''
    def input_text(self,sno,text):
        text_list = list(text)
        specific_symbol = set(['&','@','#','$','^','*'])
        for i in range(len(text_list)):
            if text_list[i] in specific_symbol:
                if i-1 < 0:
                    text_list.append(text_list[i])
                    text_list[0] = "\\"
                else:
                    text_list[i-1] = text_list[i-1] + "\\"
        seed = ''.join(text_list)
        os.popen('adb -s %s shell input text "%s"'%(sno,seed))

    def reboot_device(self,sno):
        os.popen("adb -s %s reboot"%sno)

    def capture_window(self,sno):
        os.popen("adb shell rm /sdcard/screenshot.png")
        os.popen("adb -s %s shell /system/bin/screencap -p /sdcard/screenshot.png" %sno)
        c_time = time.strftime("%Y_%m_%d_%H-%M-%S")
        os.popen("adb -s %s pull /sdcard/screenshot.png C:/Users/jayzhen/Desktop/%s.png"%(sno,c_time))


