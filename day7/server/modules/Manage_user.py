#!/usr/bin/python
#coding=utf-8

import os,sys,json,getpass
from conf import settings,template
from modules import common,logger
from dbhelper import dbapi

ftpserver_logger=logger.logger("manage_ftp_user")

class manage():
    '''
    管理用户
    :return:
    '''
    def __init__(self):
        self.all_user=dbapi.read_all_user()
        while True:
            common.show_message(template.MENU_USER,"INFO")
            choice=common.input_msg("please choice:>>")
            if choice not in ['1','2','3'] and choice.isalpha:
                common.show_message("without this choice!!!","ERROR")
                continue
            MENU_DIC={
                "1":"add_user",
                "2":"del_user",
            }
            if choice== "3":
                sys.exit()
            else:
                if hasattr(self,MENU_DIC[choice]):
                    func=getattr(self,MENU_DIC[choice])
                    func()

    def add_user(self):
        '''
        增加用户
        :return:
        '''
        try:
            while True:
                new_user=common.input_msg("please input new username:")
                if new_user == "b":
                    break
                elif new_user in self.all_user:
                    common.show_message("user:{0} is already exists!".format(new_user),"ERROR")
                    continue
                else:
                    new_user_pass=common.input_pass("please input new user {0} pass: ".format(new_user))
                    retry_pass=common.input_pass("please change again input new user {0} pass: ".format(new_user))
                    if new_user_pass != retry_pass:
                        common.show_message("The two input pass is not correct!","ERROR")
                        continue
                    else:
                        enery_pass=common.encry_sha(new_user_pass)
                        dic={'password':enery_pass,
                            'quotation':settings.HOME_QUOTA,
                            'usedspace':0,
                            }
                        user_path=os.path.join(settings.USER_INFO_PATH,new_user)
                        with open(user_path+".json",'w') as f:
                            json.dump(dic,f)
                            common.show_message("user:{0} add succ!!!".format(new_user),"NOTICE")
                            ftpserver_logger.info("user:{0} add succ!!!".format(new_user))
                            break
        except Exception as e:
            print(e)


    def del_user(self):
        '''
        删除用户
        :return:
        '''
        try:
            while True:
                dic={}
                for i,j in enumerate(self.all_user,1):
                    dic[str(i)]=j
                    print("{0}:{1}".format(i,j))
                del_chice=common.input_msg("please input your want to del user:")
                if del_chice == "b":
                    break
                elif del_chice not in dic.keys() and del_chice.isalpha:
                    common.show_message("without this choice!!!","ERROR")
                    continue
                else:
                    del_user_path=os.path.join(settings.USER_INFO_PATH,dic[del_chice])
                    os.remove(del_user_path+".json")
                    common.show_message("del user:{0} succ!!".format(dic[del_chice]),"NOTICE")
                    ftpserver_logger.info("del user:{0} succ!!".format(dic[del_chice]))
        except Exception as e:
            print(e)
