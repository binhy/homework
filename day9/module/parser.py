#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import yaml,os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings



hostconfig = settings.hosts_config
packconfig= settings.package_path

def host_info_by_ip(ip):
    """
    根据 IP 地址获取该ip对一个的服务器信息，返回一个字典
    :param ip: ip地址
    :return: 信息字典{ip:{user:'test',auth_type：1}}
    """
    return_dict = {}
    with open(hostconfig, 'r',encoding='utf8') as f:
        hosts_dict = yaml.load(f)
        host = hosts_dict[ip]
        for item in host:
            for k, v in item.items():
                return_dict[k] = v
    return {ip: return_dict}

#print(host_info_by_ip('192.168.2.129'))


def get_package_date(package_file):
    """
    执行ftp操作，从package文件读取信息，返回字典数据
    :param package_file: 处理文件
    :return: 字典信息
    """
    data_dict = {}
    with open(os.path.join(packconfig,package_file), 'r',encoding='utf8') as f:
        data = yaml.load(f)
    data_dict['exec_method'] = list(data.keys())[0]
    for method, data_info in data.items():
        for item in data_info:
            for k, v in item.items():
                data_dict[k] = v

    return data_dict

print(get_package_date("nginx.sls"))