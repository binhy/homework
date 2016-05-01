#################################################
# Created on: 2016年05月01日
# @author: 陈耀斌
# Email: 123391713@qq.com
# Blog: http://www.cnblogs.com/binhy0428/
# GitHub: https://github.com/binhy/
#################################################


一.功能说明：
本程序是一个简单版的批量主机管理程序，使用python3开发，主要功能包括：
1.需要使用帐号密码登陆批量管理主机程序
2.支持对单个或多个主机，执行命令、上传文件、下载文件
2.支持对单个或多个主机组，执行命令、上传文件、下载文件
3.记录用户操作记录
4.该程序只能使用公钥密钥连接服务器，暂时还不支持密码连接服务器
5.还没有开发管理帐号密码登陆的程序

二.运行说明:
在bin目录下运行：python3 start.py



三.用到主要知识点
1.模块：paramiko、multiprocessing、configparser、hashlib、getpass、logging
2.知识点： 多进程、函数、类、反射等



四.目录介绍：
day8/
├── bin
│   └── start.py     #主引导文件
├── conf                #配置目录
│   ├── code.py      #状态码文件
│   ├── settings.py  #系统配置文件
│   └── template.py  #模版文件
├── database            #数据目录
│   ├── host_and_group.conf   #主机和主机组设定配置文件
│   ├── init.py               #初始化主机和主机组设定配置文件
│   └── yaobin.json           #yaobin登陆用户数据文件
├── dbhelper                     #数据库操作目录
│   ├── dbapi.py              #数据库接口文件，操作数据库的都在这
├── logs                 #日志目录
│   ├── exec_log.txt  #执行日志
│   └── ssh_log.txt   #登陆日志
├── modules              #模块目录
│   ├── commands.py   #命令模块，主要逻辑都在这
│   ├── common.py     #公共模块
│   ├── logger.py     #日志模块
│   ├── main.py       #main主程序入口
│   ├── test.py       #测试文件，请忽略
│   └── User.py       #登陆用户模块
├── readme.txt           #程序讲解
└── ssh_key              #私钥存放目录
    └── id_rsa           #私钥文件


五、命令介绍
command:
        list: list [ -a | -G groupname ]                        #查看服务器信息，-a 查看没分组的全部hostname ,-G 指定组名
        cmd: cmd [ -g hostname | -G groupname ] -c command      #执行命令,-g hostname, -G 指定组名 ,-c 执行命令
        sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile  #上传下载文件，-g hostname ,-G 指定组名 ,-u 上传 ,-d 下载 ,-s 源文件路径, -t 目的文件路径
        q/quit                                                  #退出

1.  list: list [ -a | -G groupname ]
    e.g: list -a      #查看没分组的主机信息
    e.g: list -G web  #查看web组的主机信息

2. cmd: cmd [ -g hostname | -G groupname ] -c command
    e.g: cmd -g web2 -c ifconfig   #web2主机执行ifconfig 命令
    e.g: cmd -g web2,web3 -c ifconfig   #web2和web3主机执行ifconfig 命令

    e.g: cmd -G web -c ifconfig    #web主机组执行ifconfig 命令
    e.g: cmd -G web,db -c ifconfig    #web主机组和db主机组执行ifconfig 命令

3. sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile
    e.g: sftp -g web2 -u -s /tmp/test.txt  -t /tmp/test.txt  #将文件/tmp/test.txt上传到web2主机的/tmp/test.txt
    e.g: sftp -g web2,web3 -u -s /tmp/test.txt  -t /tmp/test.txt  #将文件/tmp/test.txt上传到web2主机和web3主机的/tmp/test.txt

    e.g: sftp -G web -u -s /tmp/test.txt  -t /tmp/test.txt   #将文件/tmp/test.txt上传到web主机组的/tmp/test.txt
    e.g: sftp -G web,db -u -s /tmp/test.txt  -t /tmp/test.txt   #将文件/tmp/test.txt上传到web主机组和db主机组的/tmp/test.txt

    e.g: sftp -g web2 -d -s /tmp/zabbix_agentd.pid  -t /shell/zabbix_agentd.pid  #将web2主机的/tmp/zabbix_agentd.pid下载到本机的/shell/zabbix_agentd.pid，注意：下载文件后缀会加上主机名
    e.g: sftp -g web2,web3 -d -s /tmp/zabbix_agentd.pid  -t /shell/zabbix_agentd.pid  #将web2主机和web3主机的/tmp/zabbix_agentd.pid下载到本机的/shell/zabbix_agentd.pid，注意：下载文件后缀会加上主机名

    e.g: sftp -G web -d -s /tmp/zabbix_agentd.pid  -t /shell/zabbix_agentd.pid   #将web主机组的/tmp/zabbix_agentd.pid下载到本机的/shell/zabbix_agentd.pid，注意：下载文件后缀会加上主机名
    e.g: sftp -G web,db -d -s /tmp/zabbix_agentd.pid  -t /shell/zabbix_agentd.pid   #将web主机组和db主机组的/tmp/zabbix_agentd.pid下载到本机的/shell/zabbix_agentd.pid，注意：下载文件后缀会加上主机名


六 程序运行结果展示:

[root@zabbix_monitor /python/tmp/homework/day8/bin]# python start.py

-----------------------
欢迎进入批量管理主机V0.1
-----------------------

please input username:yaobin
please input password:

----------------------------------------
command:
        list: list [ -a | -G groupname ]                        #查看服务器信息，-a 查看没分组的全部hostname ,-G 指定组名
        cmd: cmd [ -g hostname | -G groupname ] -c command      #执行命令,-g hostname, -G 指定组名 ,-c 执行命令
        sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile  #上传下载文件，-g hostname ,-G 指定组名 ,-u 上传 ,-d 下载 ,-s 源文件路径, -t 目的文件路径
        q/quit                                                  #退出

yaobin >:list -a

###############################
             default
###############################
HOSTNAME:                       IP:
lb1                                     192.168.10.3

----------------------------------------
command:
        list: list [ -a | -G groupname ]                        #查看服务器信息，-a 查看没分组的全部hostname ,-G 指定组名
        cmd: cmd [ -g hostname | -G groupname ] -c command      #执行命令,-g hostname, -G 指定组名 ,-c 执行命令
        sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile  #上传下载文件，-g hostname ,-G 指定组名 ,-u 上传 ,-d 下载 ,-s 源文件路径, -t 目的文件路径
        q/quit                                                  #退出

yaobin >:list -G db

###############################
             db
###############################
HOSTNAME:                       IP:
db_master                               192.168.10.21
db_slave                                192.168.10.4

----------------------------------------
command:
        list: list [ -a | -G groupname ]                        #查看服务器信息，-a 查看没分组的全部hostname ,-G 指定组名
        cmd: cmd [ -g hostname | -G groupname ] -c command      #执行命令,-g hostname, -G 指定组名 ,-c 执行命令
        sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile  #上传下载文件，-g hostname ,-G 指定组名 ,-u 上传 ,-d 下载 ,-s 源文件路径, -t 目的文件路径
        q/quit                                                  #退出

yaobin >:cmd -g web2,web3 -c ifconfig

HOSTNAME: web3  IP:192.168.10.33 RESULT:
em1       Link encap:Ethernet  HWaddr B0:83:FE:C4:44:72
          inet addr:192.168.10.33  Bcast:192.168.10.255  Mask:255.255.255.0
          inet6 addr: fe80::b283:feff:fec4:4472/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:15766274546 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10205743798 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:16751642478301 (15.2 TiB)  TX bytes:4955719175181 (4.5 TiB)
          Interrupt:16

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1446677892 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1446677892 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:6649348094277 (6.0 TiB)  TX bytes:6649348094277 (6.0 TiB)




HOSTNAME: web2  IP:192.168.10.32 RESULT:
em1       Link encap:Ethernet  HWaddr B0:83:FE:CF:6F:BA
          inet addr:192.168.10.32  Bcast:192.168.10.255  Mask:255.255.255.0
          inet6 addr: fe80::b283:feff:fecf:6fba/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:12915398532 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8485479119 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:13540246165489 (12.3 TiB)  TX bytes:4087617726415 (3.7 TiB)
          Interrupt:16

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1234754038 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1234754038 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:5409708807572 (4.9 TiB)  TX bytes:5409708807572 (4.9 TiB)

yaobin >:sftp -g web2,web3 -u -s /tmp/test.txt  -t /tmp/test.txt
upload src_file:/tmp/test.txt  -->>>>>>>> hostname:web2 IP:192.168.10.32 dst_file:/tmp/test.txt
upload src_file:/tmp/test.txt  -->>>>>>>> hostname:web3 IP:192.168.10.33 dst_file:/tmp/test.txt

----------------------------------------
command:
        list: list [ -a | -G groupname ]                        #查看服务器信息，-a 查看没分组的全部hostname ,-G 指定组名
        cmd: cmd [ -g hostname | -G groupname ] -c command      #执行命令,-g hostname, -G 指定组名 ,-c 执行命令
        sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile  #上传下载文件，-g hostname ,-G 指定组名 ,-u 上传 ,-d 下载 ,-s 源文件路径, -t 目的文件路径
        q/quit                                                  #退出

yaobin >:sftp -G web,db -d -s /tmp/zabbix_agentd.pid  -t /shell/zabbix_agentd.pid

###############################
             web
###############################
HOSTNAME:                       IP:
web7                            192.168.10.6
web2                            192.168.10.32
web3                            192.168.10.33

###############################
             db
###############################
HOSTNAME:                       IP:
db_master                               192.168.10.21
db_slave                                192.168.10.4
download src_file:/tmp/zabbix_agentd.pid  -->>>>>>>> hostname:web3 IP:192.168.10.33 dst_file:/shell/zabbix_agentd.pid_web3
download src_file:/tmp/zabbix_agentd.pid  -->>>>>>>> hostname:web2 IP:192.168.10.32 dst_file:/shell/zabbix_agentd.pid_web2
download src_file:/tmp/zabbix_agentd.pid  -->>>>>>>> hostname:db_master IP:192.168.10.21 dst_file:/shell/zabbix_agentd.pid_db_master
download src_file:/tmp/zabbix_agentd.pid  -->>>>>>>> hostname:web7 IP:192.168.10.6 dst_file:/shell/zabbix_agentd.pid_web7
download src_file:/tmp/zabbix_agentd.pid  -->>>>>>>> hostname:db_slave IP:192.168.10.4 dst_file:/shell/zabbix_agentd.pid_db_slave

