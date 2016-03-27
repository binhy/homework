#!/usr/bin/python
#coding=utf-8

    # 'test':
    # {'password':'456',
    # 'quotation': 1000000, #1G
    # 'usedspace':0,
    # 'expire': '2016-08-22',
    # 'is_lock':0
    #     },
    #  }
import os,re,sys
from os.path import join, getsize
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from dbhelper import dbapi
from modules import common
from conf import settings

class User(object):
    def __init__(self,username):
        self.username=username
        self.__check_users()  #实例化的时候，就马上验证用户存不存在


    def __check_users(self):
        '''
        检查用户是否存在，存在的话接着执行加载用户信息方法
        :return:
        '''
        user_list=dbapi.read_all_user()
        if self.username in user_list:
            self.exists=True     #用户存在实例变量
            self.__load_user_info()
        else:
            self.exists=False

    def __load_user_info(self):
        '''
        表示用户存在，加载用户的信息，填充对象变量
        :return:
        '''
        user_info=dbapi.read_user_by_name(self.username)
        self.password=user_info['password']
        self.quotation=int(user_info['quotation'])
        self.usedspace=int(user_info['usedspace'])
        self.homepath=os.path.join(settings.USER_HOME_FOLDER,self.username) #用户家目录
        self.currpath=self.homepath #用户当前目录

    def auth_pass(self,password):
        '''
        用户已经存在，接着用户密码验证
        :param password:
        :return:
        '''
        if password == self.password:
            return True
        else:
            return False


    def update_usedspace(self,name):
        '''
        上传完文件到服务端，最后一步是更新用户空间
        :param name: 用户名
        :return:
        '''

        size=0
        for root, dirs, files in os.walk(self.homepath):
            size+=sum([getsize(join(root, name)) for name in files])
        homepath_used_size=size/1024/1024  #计算家目录大小，相当于是计算家目录用了多少
        self.usedspace=homepath_used_size
        print(self.usedspace)
        try:
            user_info=dbapi.read_user_by_name(name)    #load指定用户的字典信息
            user_info['usedspace'] = homepath_used_size   #更新字典里面的usedspace信息
            dbapi.dump_acc(name,user_info)             #dump回去json文件
        except Exception as e:
            common.show_message("user_info or dump_acc ERROR:{0}".format(e),'ERROR')



