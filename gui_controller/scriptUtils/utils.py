# -*- coding: utf-8 -*-

import os
import platform
import re
import subprocess
import time
import exception

class AndroidUtils(object):
    def __init__(self):
        self.system = None
        self.find_type = None
        self.command = "adb"
    def judgment_system_type(self):
        #判断系统类型，windows使用findstr，linux使用grep
        self.system = platform.system()
        if self.system is "Windows":
            self.find_type = "findstr"
        else:
            self.find_type = "grep"
    def judgment_system_environment_variables(self):
        self.judgment_system_type()
        #判断是否设置环境变量ANDROID_HOME
        if "ANDROID_HOME" in os.environ:
            if self.system == "Windows":
                self.command = "adb" # os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
            else:
                self.command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        else:
            raise EnvironmentError(
                "Adb not found in $ANDROID_HOME path: %s." %os.environ["ANDROID_HOME"])

    #adb命令
    def adb(self,serialno_num,args):
        cmd = "%s -s %s %s" %(self.command, serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    #adb shell命令
    def shell(self,serialno_num,args):
        cmd = "%s -s %s shell %s" %(self.command, serialno_num, str(args))
        # if types is not None and types.has_key("read_type"):
        #     if types["read_type"] == 0:
        #         return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        #     elif types["read_type"] == 1:
        #         return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readline()
        #     elif types["read_type"] == 2:
        #         return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



    #获取设备状态
    def get_state(self,):
        return os.popen("adb -s %s get-state" %serialno_num).read().strip()

    #获取对应包名的pid
    def get_app_pid(self,pkg_name):
        if system is "Windows":
            string = shell("ps | findstr %s$" %pkg_name).stdout.read()
        else:
            string = shell("ps | grep -w %s" %pkg_name).stdout.read()
        if string == '':
            return "the process doesn't exist."
        pattern = re.compile(r"\d+")
        result = string.split(" ")
        result.remove(result[0])
        return  pattern.findall(" ".join(result))[0]

    #杀掉对应包名的进程
    def kill_process(self,pkg_name):
        pid = get_app_pid(pkg_name)
        result = shell("kill %s" %str(pid)).stdout.read().split(": ")[-1]
        if result != "":
            raise exception.SriptException("Operation not permitted or No such process")

    #获取设备上当前应用的包名与activity
    def get_focused_package_and_activity(self):
        #pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        #out = shell("dumpsys window w | %s \/ | %s name=" %(find_util, find_util)).stdout.read()

        #return pattern.findall(out)[0]
        return shell("dumpsys activity | findstr mFocusedActivity").stdout.read().split()[-1][:-1]

    #获取当前应用的包名
    def get_current_package_name(self):
        return get_focused_package_and_activity().split("/")[0]

    #获取当前设备的activity
    def get_current_activity(self):
        return get_focused_package_and_activity().split("/")[-1]

    #时间戳
    def timestamp(self):
        return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

    def get_device_list(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        result.reverse()  #将readlines结果反向排序
        for line in result[1:]:
            if "attached" not in line.strip():
                devices.append(line.split()[0])
            else:
                break
        return devices

# if __name__ == "__main__":
#     a = AndroidUtils()
#     a.judgment_system_environment_variables()
#     print a.get_device_list()
