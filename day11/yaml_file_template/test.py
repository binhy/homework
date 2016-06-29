#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import yaml


def yaml_parser(yml_file):
    '''
    加载yaml文件，返回数据
    :param yml_file:
    :return:
    '''
    try:
        yaml_file=open(yml_file,'r')
        data=yaml.load(yaml_file)
        return data
    except Exception as e:
        print(e)


a=yaml_parser("create_bindhosts.yaml")
print(a.items())
for key,val in a.items():
    print(key,val)