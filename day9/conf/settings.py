#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import os,sys,yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

hosts_config = os.path.join(BASE_DIR, "conf/hosts.yaml")

# 配置文件 package 包存放目录,用来存放执行命令的 yaml文件
package_path = os.path.join(BASE_DIR, "package")


# with open(hosts_config,'r',encoding='utf8') as f:
#     host_dict=yaml.load(f)
#     print(host_dict)
#     t=host_dict['192.168.2.129']
#     print(t)
#     for item in t:
#         for k,v in item.items():
#             print(k,v)

# data_dict={}
# with open(os.path.join(package_path,"nginx.sls"),'r',encoding='utf8') as f:
#     data=yaml.load(f)
#     print(data)
#     data_dict["exec_method"]=list(data.keys())[0]
#     print(data_dict)
#     for method,host_info in data.items():
#         print(method,host_info)
#         for item in host_info:
#             for k,v in item.items():
#                 data_dict[k]=v
#
# print(data_dict)