#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import sys
from modules import common,User,logger,commands
from dbhelper import dbapi
from conf import template
from conf.code import login_code


login_log=logger.logger("login_user","ssh_log.txt")

def main():
    while True:
        print(template.WELCOME_MENU)
        username=common.input_msg("please input username:")
        user_inst=User.User(username)
        if user_inst.is_locked==1:  #用户被锁
            common.show_message(login_code["102"].format(username),"CRI")
            break
        elif not user_inst.exists:  #用户不存在
            common.show_message(login_code["103"].format(username),"WARN")
            login_log.error(login_code["103"].format(username))
            break
        else:
            trycount=0
            count = 3
            while trycount < count:  #尝试输错密码<3次
                password=common.input_msg("please input password:")  #这里最后要换成getpass的，即是input_pass
                if not user_inst.user_auth(password): #认证密码错误
                    common.show_message(login_code["104"].format(username),"ERR")
                    login_log.error(login_code["104"].format(username))
                    trycount+=1
                    continue
                else:  #登陆成功
                    exit_flag=False
                    while not exit_flag:
                        print(template.MAIN_MENU)
                        command_str=input("{username} >:".format(username=username))
                        if command_str.strip().lower() == "q" or command_str.strip().lower() == "quit":
                            sys.exit()
                        else:
                            commands.exec(command_str)
            else:  #输错3次密码，锁定该帐号
                common.show_message(login_code["105"].format(username),'CRI')
                login_log.error(login_code["105"].format(username))
                user_inst.locked()
                sys.exit()



