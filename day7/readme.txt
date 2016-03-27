#################################################
# Created on: 2016年03月27日
# @author: 陈耀斌
# Email: 123391713@qq.com
# Blog: http://www.cnblogs.com/binhy0428/
# GitHub: https://github.com/binhy/
#################################################


ftp小程序 README
===============


功能说明：
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


 目录介绍：
 client/
├── bin
│   └── client_start.py  #主引导文件
├── conf                  #配置目录
│   ├── codes.py       #状态码文件
│   ├── settings.py    #系统配置文件
│   └── template.py    #模板文件
├── logs                  #记录日志目录
│   └── ftpclient.log  #记录日志文件
└── modules               #模块目录
    ├── client.py         #客户端类文件，主要的逻辑都在这
    ├── common.py         #公共模块文件
    ├── logger.py         #日志定义文件

--------------------------------------------------------------

server/
├── bin
│   ├── ftp_start.py
│   └── manage_user.py
├── conf
│   ├── settings.py
│   └── template.py
├── database
│   ├── sample.py
│   └── User
│       ├── test.json
│       └── yaobin.json
├── dbhelper
│   ├── dbapi.py
├── logs
│   └── ftpserfer.log
├── modules
│   ├── common.py
│   ├── logger.py
│   ├── main.py
│   ├── Manage_user.py
│   ├── server.py
│   └── User.py
└── uploads
    └── yaobin

