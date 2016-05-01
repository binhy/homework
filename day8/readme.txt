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
 client/
├── bin
│   └── client_start.py  #主引导文件
├── conf                  #配置目录
│   ├── codes.py       #状态码文件
│   ├── settings.py    #系统配置文件
│   └── template.py    #模板文件
├── download              #用户下载文件存放目录
│   └── test.txt       #下载测试文件test.txt
├── logs                  #记录日志目录
│   └── ftpclient.log  #记录日志文件
└── modules               #模块目录
    ├── client.py         #客户端类文件，主要的逻辑都在这
    ├── common.py         #公共模块文件
    ├── logger.py         #日志定义文件

--------------------------------------------------------------

server/
├── bin
│   ├── ftp_start.py    #主程序ftp启动文件
│   └── manage_user.py  #主程序ftp管理用户文件
├── conf                   #配置目录
│   ├── settings.py     #系统配置文件
│   └── template.py     #模板文件
├── database               #用户数据库目录
│   ├── sample.py       #请忽略
│   └── User            #User用户数据目录
│       ├── test.json   #test用户数据文件
│       └── yaobin.json  #yaobin用户数据文件
├── dbhelper               #数据库操作接口目录
│   ├── dbapi.py        #数据库操作接口文件
├── logs                   #ftp-server端日志目录
│   └── ftpserfer.log   #ftp-server端日志文件
├── modules                #模块目录
│   ├── common.py       #公共模块
│   ├── logger.py       #日志定义文件
│   ├── main.py         #main主程序入口
│   ├── Manage_user.py  #管理用户文件
│   ├── server.py       #服务端类文件，主要的逻辑都在这
│   └── User.py         #服务端实例化用户类文件
└── uploads                #上传目录
    └── yaobin             #yaobin用户的家目录

