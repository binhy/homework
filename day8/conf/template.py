#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'


WELCOME_MENU='''\033[1;32m
-----------------------
欢迎进入批量管理主机V0.1
-----------------------
\033[0m'''


MAIN_MENU='''\033[1;35m
----------------------------------------
command:
        list: list [ -a | -G groupname ]                        #查看服务器信息，-a 查看没分组的全部hostname ,-G 指定组名
        cmd: cmd [ -g hostname | -G groupname ] -c command      #执行命令,-g hostname, -G 指定组名 ,-c 执行命令
        sftp: sftp [ -g hostname | -G groupname ] [ -u | -d ] -s srcfile -t destfile  #上传下载文件，-g hostname ,-G 指定组名 ,-u 上传 ,-d 下载 ,-s 源文件路径, -t 目的文件路径
        q/quit                                                  #退出
\033[0m'''


GROUP_MENU='''\033[1;36m
###############################
             {0}
###############################
\033[0m'''


#print(MAIN_MENU)