#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import os,sys,logging

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


#数据存放目录(登陆用户密码、分组信息，)
db_file=os.path.join(BASE_DIR,"database")
#日志水平
LOG_LEVEL = logging.INFO
#日志文件存放路径
LOGS_PATH=os.path.join(BASE_DIR,"logs")
#加密私钥文件存放目录
rsa_file_path=os.path.join(BASE_DIR,"ssh_key")
#加密私钥文件密码
rsa_file_pass="binhy0428"

