#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import sys,time,yaml

def input_msg(message):
    """
    判断input输入的信息是否为空的公共检测函数
    :param message: input()函数的提示信息
    :return: 返回输入的信息
    """
    while True:
        input_value = input("\033[1;32m{0}\033[0m".format(message)).strip().lower()
        if len(input_value) == 0:
            color_print("not allow null! please change again!",exits=True)
            continue
        else:
            return input_value

def color_print(msg,color='',exits=False):
    '''
    颜色打印输出或者退出
    :param msg:
    :param color:
    :param exits:
    :return:
    '''
    color_msg={
        'blue':'\033[1;36m{0}\033[0m',
        'green':'\033[1;32m{0}\033[0m',
        'yellow':'\033[1;33m{0}\033[0m',
        'red':'\033[1;31m{0}\033[0m',
        'gray':'\033[1;37m{0}\033[0m',
        'title':'\033[30;42m{0}\033[0m',
        'info':'\033[32m{0}\033[0m',
    }
    msg=color_msg.get(color,'\033[1;31m{0}\033[0m').format(msg)  #如果没有找到key，返回红色,即是默认就是红色
    print(msg)
    if exits:
        time.sleep(2)
        sys.exit()
    else:
        return msg



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
        color_print(e)




