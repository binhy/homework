#!/usr/bin/python
#coding=utf-8

#连接
CONN_SUCC = 200             #连接ftp-server成功
CONN_FAIL = 500             #连接ftp-server失败

#认证
AUTH_SUCC = 201             #登陆认证成功
AUTH_USER_ERROR = 600       #登陆认证，用户不存在
AUTH_FAIT_PASS = 601        #登陆认证失败，错误的密码
#AUTH_LOCKED = 602           #用户已经被锁


#文件上传
FILE_UPLOAD_SUCC = 202      #文件上传成功
FILE_UPLOAD_FAIL = 700      #文件上传失败
FILE_NOT_EXISTS = 701       #文件不存在
IS_DIR=704                  #这是一个目录
IS_FILE=705                 #这是一个文件
TRANS_READY = 703           #上传或者下载文件，客户端已经准备ready


#磁盘配额
DISK_ENOUGH=203             #磁盘空间足够
DISK_NOT_ENOUGH=800         #磁盘空间不足够


#删除文件
DEL_FILE_SUCC=204           #删除文件成功
DEL_FILE_FAIL=900           #删除文件失败

#删除目录
DEL_DIR_SUCC=205            #删除目录成功
DEL_DIR_FAIL=1000           #删除目录失败
DIR_NOT_EXISTS=1001         #目录不存在




