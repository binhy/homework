#!/usr/bin/python
#coding=utf-8

import hashlib,getpass,io,sys

def show_message(msg,msgtype):
    '''
    对print函数进行封装，根据不同类型显示不同颜色
    :param msg: 显示的消息体
    :param msgtype: 消息类型
    :return:
    '''
    if msgtype =='NOTICE':
        print('\n\033[1;32m{0}\033[0m\n'.format(msg))
    elif msgtype == 'ERROR':
        print('\n\033[1;31m{0}\033[0m\n'.format(msg))
    elif msgtype == 'INFO':
        print('\n\033[1;33m{0}\033[0m\n'.format(msg))


def input_msg(message):
    """
    判断input输入的信息是否为空的公共检测函数
    :param message:
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
    """
    用户密码加密函数 sha224加密
    :param string: 明文字符串
    :return: 加密字符串
    """
    sha=hashlib.sha224()
    sha.update(string.encode())
    sha_value=sha.hexdigest()
    return sha_value


def encry_md5(file):
    """
    获取文件的MD5值，用于MD5校验
    :param file: 文件名
    :return: MD5值
    """
    fmd = hashlib.md5()
    file = io.FileIO(file, 'r')
    byte = file.read(2048)
    while byte != b'':
        fmd.update(byte)
        byte = file.read(2048)
    file.close()
    md5value = fmd.hexdigest()
    return md5value


def print_process(curr_size,total_size):
    '''
    打印进度条，打印66个#
    :param curr_size:
    :param total_size:
    :return:
    '''

    i = int((curr_size/total_size) * 100)
    j = int((curr_size/total_size) * 66)
    p="#"*j
    sys.stdout.write("[{0}%] || {1}\r".format(str(i),p))
    sys.stdout.flush()


