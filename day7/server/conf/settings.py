#!/usr/bin/python
#coding=utf-8


import os
import sys
import logging


BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


#服务端地址
FTP_SERVER_IP='127.0.0.1'
FTP_SERVER_PORT=1235
#日志文件存放路径
LOGS_PATH=os.path.join(BASE_DIR,"logs/ftpserfer.log")
#日志水平
LOG_LEVEL = logging.INFO
#用户信息文件保存数据库路径
USER_INFO_PATH=os.path.join(BASE_DIR,"database/User")
#用户家目录文件夹
USER_HOME_FOLDER=os.path.join(BASE_DIR,"uploads")
#客户端家目录最大上传文件大小(默认配置)，单位MB
HOME_QUOTA=500


