**注意：修改模块名后，记得将类中的import修改，还要清除一下原先编译好的pyc文件**

技术实现所使用到的python模块：
    1.time
    2.re
    3.easygui   （三方）
    4.wx        （三方）
    5.os
    6.bs4.BeaufulSoup   （三方）
    7.urllib,urllib2,urlparse
    8.requests   （三方）

ADB环境变量设置(android sdk)：
    1.ANDROID_HONE:T:\Android\sdk
    2.path:%ANDROID_HOME%\build-tools\24.0.1;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;

使用到的adb命令：
    1.adb devices  查看连接上电脑的所有手机设备
    2.adb -s sno shell cat /system/build.prop  通过查看手机系统文件查看设备信息
            ro.build.version.release=4.0.3(android版本
            ro.product.model=S2(手机型号)--
            ro.product.brand=Spreadtrum(手机品牌)
            ro.product.name=sp6825eb_7661plus(手机正式名称)
            ro.product.device=sp6825eb_7661（采用的设备）
            ro.product.board=sp6825eb_7661（采用的主板）
            ro.product.cpu.abi=armeabi-v7a（cpu的版本）
            ro.product.cpu.abi2=armeabi(CPU品牌)
            ro.product.manufacturer=Spreadtrum(手机制造商)
    3.adb -s %s shell getprop dhcp.wlan0.ipaddress 获取手机的ip地址
    4.adb -s %s shell getprop ro.sf.lcd_density   获取手机的dpi值
    5.adb -s %s shell wm size 获取手机的分辨率
    6.adb install packagename  安装文件
    7.adb uninstall packagename  卸载文件
    8.adb shell pm list packages  显示已安装的所有安装包（包括系统和第三方）
    9.adb shell pm clear packagename  清除应用的数据（初始化）
    10.aapt dunmp badging package_name 查看apk文件的信息

需求：

第一版：
    1.实现获取网页并下载网页中的apk文件（爬虫技术）。
    2.连接手机，并将下载的apk文件安装到手机上。

第二版：
    1.在第一版的基础上，实现gui界面。
    2.在gui界面上展示设备信息和apk文件列表。

第三版：
    1.添加button按钮能够刷新设备信息。
    2.添加按钮下载按钮。
    3.添加刷新按钮。

总结：
    1.针对需求，首先是先实现相应的功能，随后在使用三方的桌面设计库再进行界面可视化设计。
    2.编程过程中有遇到技术上的问题，如：文件夹的更新。
    3.技术优化：可以使用多线程机制来消除ANR现象。
    4.功能还可拓展，如：内存的监控，耗时，monkey执行和日志分析等。
    5.adb环境下的功能有很多都集成在ddms工具中，想方便日常工作，可以继续设计需求并实现。
    6.可以将一些常量进行文件化配置。


第四版修改需求：
    1.可以有覆盖安装
    2.修改获取手机分辨率的方式
    3.下载时提示apk包的时间（页面获取的时间，将时间添加到文件名中）
    4.修改gui显示界面的布局（原先是上下俩个box，下面有分为左右box;现修改为上中下三个box

第五版修改需求：
    1.添加截图功能
    2.使用requests替换urllib

第六版修改需求：
    1.使用subprocess.Popen代替os.popen




