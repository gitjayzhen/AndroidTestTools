# -*- coding: utf-8 -*-

import os
import platform
import re
import subprocess
import time
import exception
import string
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')


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

    #杀掉对应包名的进程；另一个方式使用adb shell am force-stop pkg_name
    def kill_process(self,pkg_name):
        pid = get_app_pid(pkg_name)
        result = shell("kill %s" %str(pid)).stdout.read().split(": ")[-1]
        if result != "":
            raise exception.SriptException("Operation not permitted or No such process")

    #获取设备上当前应用的包名与activity
    def get_focused_package_and_activity(self,sno):
        return self.shell(sno,"dumpsys activity | findstr mFocusedActivity").stdout.read().split()[-2]

    #获取当前应用的包名
    def get_current_package_name(self,sno):
        return self.get_focused_package_and_activity(sno).split("/")[0]

    #获取当前设备的activity
    def get_current_activity(self,sno):
        return self.get_focused_package_and_activity(sno).split("/")[-1]

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

    def stop_and_restart_5037(self):
        pid1 = os.popen("netstat -ano | findstr 5037 | findstr  LISTENING").read()
        if pid1 is not None:
            pid = pid1.split()[-1]
        #下面的命令执行结果，可能因电脑而异，若获取adb.exe时出错，可自行调试！
        #E:\>tasklist /FI "PID eq 10200"
        #Image Name                     PID Session Name        Session#    Mem Usage
        #========================= ======== ================ =========== ============
        #adb.exe                      10200 Console                    1      6,152 K

        process_name = os.popen('tasklist /FI "PID eq %s"' %pid).read().split()[-6]
        process_path = os.popen('wmic process where name="%s" get executablepath' %process_name).read().split("\r\n")[1]

        # #分割路径，得到进程所在文件夹名
        # name_list = process_path.split("\\")
        # del name_list[-1]
        # directory = "\\".join(name_list)
        # #打开进程所在文件夹
        # os.system("explorer.exe %s" %directory)
        #杀死该进程
        os.system("taskkill /F /PID %s" %pid)
        os.system("adb start-server")

    '''
    2016.12.20获取当前所有运行的活动（运行的app）
    '''
    def get_running_activity(self):
        getActivityCmd = "adb shell dumpsys activity activities"
        tempString = os.popen(getActivityCmd).read()
        returnString = []
        startIndex = 0
        tempString = tempString.split('\n')
        for line in tempString:
            line = line.strip()
            if line:
                returnString.append(line)
        #使用了枚举方式
        for index,line in enumerate(returnString):
            if "Running activities" in line:
                startIndex = index
                break
        returnList = returnString[startIndex:startIndex+3]
        return returnList[-1]

    """
    2017.01.12 @pm 添加系统在4.4.x(sdk>19)以上手机可以进行截取屏幕视频动画的功能
               @func 判断系统->执行任务->获取结果
    """
    def get_srceenrecord(self,sno,times,path):
        PATH = lambda p: os.path.abspath(p)
        sdk = string.atoi(self.shell(sno,"getprop ro.build.version.sdk").stdout.read())
        try:
            times = string.atoi(times)
        except ValueError, e:
            print ">>>Value error because you enter value is not int type, use default 'times=20s'"
            times = int(20)
        if sdk >= 19:
                self.shell(sno,"screenrecord --time-limit %d /data/local/tmp/screenrecord.mp4"%times).wait()
                print ">>>Get Video file..."
                time.sleep(1.5)
                path = PATH(path)
                if not os.path.isdir(path):
                    os.makedirs(path)
                self.adb(sno,"pull /data/local/tmp/screenrecord.mp4 %s"  %PATH("%s/%s.mp4" %(path, self.timestamp()))).wait()
                self.shell(sno, "rm /data/local/tmp/screenrecord.mp4")
                print ">>>ok"
        else:
            print "sdk version is %d, less than 19!" %sdk
            sys.exit(0)
    """
    2017.01.13 @pm 杀死进程同在设置中强制关闭一个程序
               @func get到sno和package，进行命令执行
    """
    def execute_kill_specified_process(self,sno,specified_package):
        self.shell(sno, "am force-stop %s"%specified_package)

    """
    2017.01.13 @pm #获取设备上当前应用的权限列表
                   #Windows下会将结果写入permission.txt文件中，其他系统打印在控制台
    """
    def get_permission_list(self,sno,package_name):
        PATH = lambda p: os.path.abspath(p)
        permission_list = []
        result_list = self.shell(sno,"dumpsys package %s | findstr android.permission" %package_name).stdout.readlines()
        for permission in result_list:
            permission_list.append(permission.strip())
        pwd = os.path.join(os.getcwd(),"gui_controller\\scriptUtils")
        permission_json_file = file("%s\\permission.json"%pwd)
        file_content = json.load(permission_json_file)["PermissList"]
        name = "_".join(package_name.split("."))
        f = open(PATH("%s\\%s_permission.txt" %(pwd,name)), "w")
        f.write("package: %s\n\n" %package_name)
        for permission in permission_list:
            for permission_dict in file_content:
                if permission == permission_dict["Key"]:
                    f.write(permission_dict["Key"] + ":\n  " + permission_dict["Memo"] + "\n")
        f.close




