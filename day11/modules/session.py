#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

from conf import settings,template
from modules import common,models,ssh_login
from sqlalchemy import create_engine,Table
from  sqlalchemy.orm import sessionmaker


class start_session(object):
    def __init__(self):
        self.engine = create_engine(settings.DB_CONN,echo=False)
        self.SessionCls = sessionmaker(bind=self.engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
        self.session = self.SessionCls()
        self.start()


    def auth(self):
        count = 0
        while count <3:
            user_name =common.input_msg("please input your username>:")
            passwd=common.input_msg("please input your passwd>:")
            user_obj=self.session.query(models.UserProfile).filter(models.UserProfile.username==user_name,
                                                                   models.UserProfile.password==passwd).first()
            if user_obj:
                return user_obj
            else:
                print("username or password not correct!")
                count += 1
        else:
            common.color_print("Too many retrys !",exits=True)

    def start(self):
        self.user=self.auth()
        if self.user:
            print(template.WELCOME_MENU.format(self.user.username))
            common.color_print(self.user.bind_hosts,color="green")
            common.color_print(self.user.groups,color="green")
            exit_flag = False
            while not exit_flag:
                if self.user.bind_hosts:
                    pass
                for index,group in enumerate(self.user.groups):
                    pass

                choice=common.input_msg("{0}".format(self.user.username))
                if choice == "z":
                    pass
                    for index,bind_host in enumerate(self.user.bind_host):
                        pass

                elif choice.isdigit():
                    choice = int(choice)
                    if choice < len(self.user.groups):
                        pass
                        for index,bind_host in enumerate(self.user.groups[choice].bind_hosts):
                            pass


                        while not exit_flag:
                            user_option = common.input_msg("")
                            if user_option =="b": break
                            if user_option == "q": exit_flag=True
                            if user_option.isdigit():
                                user_option = int(user_option)

                                ssh_login.ssh_login(self.user,self.user.groups[choice].bind_hosts[user_option],
                                                    self.session,log_recoreding)
                    else:
                        common.color_print("no this option",exits=False)