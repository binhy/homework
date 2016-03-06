#!/usr/bin/env python
#coding=utf-8
__author__ = 'yaobin'

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(base_dir)
sys.path.append(base_dir)


import os
import json
import re
import time
from core import db_handler
from conf import settings


def load_all_role_name():
    '''
    返回全部游戏角色列表
    '''
    db_path=db_handler.db_handler(settings.ROLE_DATABASE)
    all_role_name_list=os.listdir(db_path)
    all_name=[]
    for i in all_role_name_list:
        name=re.findall(r'(\w+).json',i)
        all_name.append(name[0])
    return all_name


def load_role_acc(role_name):
    '''
    load 指定角色名数据
    :param role_name:
    :return: 角色数据
    '''
    db_path = db_handler.db_handler(settings.ROLE_DATABASE)
    account_file = "%s/%s.json" %(db_path,role_name)
    with open(account_file) as f:
        acc_data = json.load(f)
        return  acc_data



def dump_role_acc(role_data):
    '''
    更新了角色数据之后，写回到文件
    :param role_data:
    :return:
    '''
    db_path = db_handler.db_handler(settings.ROLE_DATABASE)
    account_file = "%s/%s.json" %(db_path,role_data['name'])
    with open(account_file, 'w') as f:
        acc_data = json.dump(role_data,f)

    return True


def load_weapon_dic():
    '''
    load 武器商品字典
    :param
    :return: 武器商品字典
    '''
    db_path = db_handler.db_handler(settings.WEAPON_DATABASE)
    account_file = "%s/weapon_list.json" %(db_path)
    with open(account_file) as f:
        acc_data = json.load(f)
        return  acc_data


def dump_we_acc(we_data):
    '''
    更新了商品数据之后，写回到文件
    :param we_data:
    :return:
    '''
    db_path = db_handler.db_handler(settings.WEAPON_DATABASE)
    account_file = "%s/weapon_list.json" %(db_path)
    with open(account_file, 'w') as f:
        acc_data = json.dump(we_data,f)

    return True

#a=load_all_role_name()
#print(a)