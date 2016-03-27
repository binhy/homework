#################################################
# Created on: 2016年03月27日
# @author: 陈耀斌
# Email: 123391713@qq.com
# Blog: http://www.cnblogs.com/binhy0428/
# GitHub: https://github.com/binhy/
#################################################


一.功能说明：
本程序是一个模拟 FTP 的应用，包括客户端和服务端，实现如下功能：
 1 可以实现多客户端连接, 服务端采用 SocketServer 模块实现，支持多客户端连接
 2 实现客户端登录验证,  对客户端登录时采用 sha224 加密算法进行加密,
 3 对用户访问目录进行限制，只允许在自己家目录下进行访问，不能进入其他用户目录
 4 对用户上传目录磁盘进行限制，默认500M
 5 支持文件上传、下载的进度显示
 6 支持删除、添加用户
 6 支持一下命令功能
   put: 上传文件
   get: 下载文件
   ls: 显示文件夹内容
   cd:  目录切换
   rmf: 删除文件
   rmd: 删除目录


二.运行说明:
服务端启动ftp：python3 ftp_start.py start
服务端管理ftp用户：python3 manage_user.py
客户端连接ftp：python3 client_start.py -s 地址 -p 端口



三.用到主要知识点
1.模块：socket, socketserver, hashlib(md5,sha224),json,getpass,logging,shutil 等
2.知识点： 多线程、函数、类、反射等



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

