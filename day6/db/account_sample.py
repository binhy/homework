#!_*_coding:utf-8_*_
#__author__:"Alex Li"


import json
acc_dic = {
    'name': "yaobin",  #名字
    'role': 'man',     #角色
    'weapon': "AK47",  #手持武器
    'weapon_list':[], #武器库列表
    'grade': 0,      #等级
    'blood_volume': 100,  #血量
    'exp': 0,   #经验值
    'money': 0,   #钱
}

print(json.dumps(acc_dic))