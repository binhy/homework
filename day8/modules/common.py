#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'
"""
公共函数模块
"""

import hashlib,getpass


def input_msg(message):
    """
    判断input输入的信息是否为空的公共检测函数
    :param message: input()函数的提示信息
    :return: 返回输入的信息
    """
    while True:
        input_value = input(message).strip().lower()
        if len(input_value) == 0:
            show_message("not allow null! please change again!","ERROR")
            continue
        else:
            return input_value


def input_pass(message):
    '''
    getpass 会显示提示字符串, 关闭键盘的屏幕反馈, 然后读取密码.
    :param message:
    :return: 密码
    '''
    while True:
        input_value=getpass.getpass(message)
        if len(input_value) == 0:
            show_message("not allow null password! please change again!","ERROR")
            continue
        else:
            return input_value


def encry_sha(string):
    '''
    用户登陆密码加密
    :param string: 明文密码字符串
    :return: sha1加密后的字符串
    '''

    m =hashlib.sha1()
    m.update(string.encode())
    result=m.hexdigest()
    return result



def show_message(msg,msgtype):
    '''
    对print函数进行封装，根据不同类型显示不同颜色
    :param msg: 需要显示的消息
    :param msgtype: 消息类型
    :return:
    '''
    if msgtype =='INFO':     #信息
        print('\033[1;32m{0}\033[0m'.format(msg))
    elif msgtype == 'WARN':  #警告
        print('\033[1;33m{0}\033[0m'.format(msg))
    elif msgtype == 'ERR':   #错误
        print('\033[1;31m{0}\033[0m'.format(msg))
    elif msgtype == 'CRI':   #临界,严重
        print('\033[1;37m{0}\033[0m'.format(msg))



# a=encry_sha('123')
# print(a)