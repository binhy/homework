#!/usr/bin/env python
#coding=utf-8

import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)

#初始化角色数据
init_role_data={
    'name': None,  #名字
    'role': 'man',     #角色
    'weapon': "knife",  #手持武器
    'weapon_list':[], #武器库列表
    'grade': 0,      #等级
    'blood_volume': 100,  #血量
    'exp': 0,   #经验值
    'money': 0,   #钱
}

#初始化故事：
STORY = ['我有一个可恶的女朋友叫大肥妹', '我们在大学认识，被我捕获了', '突然有一天我掉进大海，我穿越到了小游戏', '当我醒来的时候，天使引领者出现在我面前']


#角色数据库
ROLE_DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'game_accounts',
    'path': "%s/db" % BASE_DIR
}

#商品武器库
WEAPON_DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'weapon_shop',
    'path': "%s/db" % BASE_DIR
}






