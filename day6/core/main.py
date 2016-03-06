#!/usr/bin/env python
#coding=utf-8
__author__ = 'yaobin'

import os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(base_dir)
sys.path.append(base_dir)


from conf import settings
#from role import already_role
from core import dump_or_load
from core import scene
from role.role import hero,girl,we_person,already_role





def new_game():
    '''
    新游戏函数
    :return
    '''

    heroine=girl("heroine") #实例化天使引领者
    input("欢迎你进入回到10年前小游戏")
    while True:
        name=input("\033[32;1m请输入您的游戏名字:\033[0m").strip()
        already_role_dic=already_role()  #获取已经存在角色字典
        if name and name not in already_role_dic.values():
            role_dic=settings.init_role_data
            role_dic['name']=name
        else:
            print("\033[31;1m名字已经存在或者你输入的是空值！请重新输入！\033[0m")
            continue
        try:
            new_role=hero(role_dic)  #实例化一个新的男主角角色
        except Exception as e:
            print("\033[31;1m不能为空！请重新输入！\033[0m")
            continue
        #print(new_role.hero_dic)
        for i in settings.STORY:
            input(i)
        new_role.say('我擦，我怎么在这里')
        heroine.say('你已经穿越进来10年前！')
        new_role.say('那么吊，我想回到现实世界！！')
        heroine.say('请完成你自己的修炼！再来找我！')
        input("于是我眼前出现了3个选择：")
        we_busman=we_person('businessman') #实例化一个武器商人
        choice_scene=scene.all_scene(new_role,we_busman,heroine) #实例化场景
        choice_scene.choice_scene() #执行场景对象的方法choice_scene，进入场景后要干嘛








def old_game():
    '''
    旧角色游戏
    :return:
    '''
    heroine=girl("heroine")  #实例化天使引领者
    while True:
        already_role_dic=already_role()
        for key,val in already_role_dic.items():
            print(key,val)   #打印存在的角色
        choice_num=input("\033[32;1m 请选择你要进入游戏的人物：\033[0m")
        if choice_num =="r":
            break
        try:
            your_choice_role=already_role_dic[int(choice_num)]
        except Exception as e:
            print("\033[31;1m 没有这个人物，请重新输入！\033[0m")
            continue
        if your_choice_role:
            Role_dic=dump_or_load.load_role_acc(your_choice_role)
            if Role_dic:
                old_role=hero(Role_dic) #实例化一个旧角色
                we_busman=we_person('businessman') #实例化一个武器商人
                choice_scene=scene.all_scene(old_role,we_busman,heroine)  #实例化场景
                choice_scene.choice_scene()  #执行场景对象的方法choice_scene，进入场景后要干嘛


def exit():
    '''
    退出游戏
    :return:
    '''
    sys.exit()




def run():
    '''
    主调用函数
    :return:
    '''
    main_menu_dic={1:old_game,2:new_game,3:exit}
    break_flag=False
    while not break_flag:
        mess='''\033[33;1m
请选择1,选择已经存在的游戏角色  2,创建新的游戏角色 3,退出
            \033[0m'''
        ret=input(mess)
        if len(ret)>0 and int(ret) in main_menu_dic:
            main_menu_dic[int(ret)]()
        else:
            print("\033[31;1m 没有这个选择，请重新选择 \033[0m")










