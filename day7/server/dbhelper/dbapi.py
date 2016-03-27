#!/usr/bin/python
#coding=utf-8


import os,re,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import json
from conf import settings
from modules import common



def read_all_user():
    '''
    返回全部用户列表
    '''
    db_path=settings.USER_INFO_PATH
    all_role_name_list=os.listdir(db_path)
    all_name=[]
    for i in all_role_name_list:
        name=re.findall(r'(\w+).json',i)
        all_name.append(name[0])
    return all_name


def read_user_by_name(name):
    '''
    根据用户名，获取一个用户的信息
    :param name: 用户名
    :return: 返回一个用户信息字典
    '''
    db_path=settings.USER_INFO_PATH
    account_file="%s/%s.json" %(db_path,name)
    with open(account_file) as f:
        acc_data=json.load(f)
    return acc_data

def dump_acc(name,user_info):
    '''
    更新了用户数据之后，写回到文件
    :param name: 用户名
    :param user_info:  用户信息字典
    :return:
    '''

    db_path = settings.USER_INFO_PATH
    account_file = "%s/%s.json" %(db_path,name)
    with open(account_file, 'w') as f:
        acc_data = json.dump(user_info,f)
    return True

# def lock_user(name):
#     '''
#     锁定用户方法
#     :param name:
#     :return:
#     '''
#     db_path=settings.USER_INFO_PATH
#     account_file="%s/%s.json" %(db_path,name)
#     user_info=read_user_by_name(name)
#     user_info["is_lock"] =1
#     with open(account_file,"w") as f:
#         acc_data=json.dump(user_info,f)
#     return True


