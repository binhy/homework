#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

from conf import settings,code
from modules import  common,logger
from dbhelper import dbapi
#from modules.myexception import MyException

login_log=logger.logger("login_user","ssh_log.txt")

class User(object):

    def __init__(self,uname):
        self.username=uname
        self.password=""
        self.is_locked=""
        self.exists=True
        self.__load_user_info()



    def __load_user_info(self):
        '''
        实例化对象之后，马上load这个用户的信息
        :return:
        '''
        try:
            self.user_dict=dbapi.load_login_db_user(self.username)
            if self.user_dict:
                self.password=self.user_dict['password']
                self.is_locked=self.user_dict['is_locked']
            else:
                self.exists=False
                raise exec.login_code["101"]
        except Exception as e:
            login_log.error(e)


    def user_auth(self,password):
        '''
        认证密码
        :param password: 密码
        :return: 认证通过返回True，失败False
        '''
        try:
            encry_passwd = common.encry_sha(password)
            if self.password == encry_passwd:
                return True
            else:
                login_log.error()
                return False
        except Exception as e:
            login_log.error(e)



    def locked(self):
        '''
        输错密码超过3次，锁定该用户
        :return:
        '''
        try:
            self.user_dict=dbapi.load_login_db_user(self.username)
            dbapi.lock_user(self.user_dict,self.username)
        except Exception as e:
            login_log.error(e)

