#!/usr/bin/python
#coding=utf-8

'''
客户端配置文件
'''

import os
import sys
import logging


BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
sys.path.append(BASE_DIR)


#服务端地址
FTP_SERVER_IP="127.0.0.1"
FTP_SERVER_PORT='1234'
#文件下载保存路径
DOWNLOAD_FILE_PATH = os.path.join(BASE_DIR,"download")
#日志文件存放路径
LOGS_PATH=os.path.join(BASE_DIR,"logs/ftpclient.log")
#日志水平
LOG_LEVEL = logging.INFO

