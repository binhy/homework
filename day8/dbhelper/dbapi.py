#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'





import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json,configparser
from conf import settings,template
from conf.code import exec_code
from modules import common,logger


exec_log=logger.logger("exec_log","exec_log.txt")

def load_login_db_user(username):
    '''
    加载用户json
    :param username: 用户名
    :return: 用户字典信息
    '''
    user_path=os.path.join(settings.db_file,username+'.json')
    if os.path.exists(user_path):
        with open(user_path,'r') as f:
            user_dict=json.load(f)
            return user_dict
    else:
        return False



def lock_user(user_dict,username):
    '''
    输错3次密码，锁定该用户
    :param user_dict:用户字典信息
    :param username:  用户名
    :return:
    '''
    user_path=os.path.join(settings.db_file,username+'.json')
    with open(user_path,'w') as f:
        user_dict['is_locked'] =1
        json.dump(user_dict,f)



def load_default_host():
    '''
    加载全部没有分组的host出来
    :return: 全部没有分组的host
    '''
    host_path=os.path.join(settings.db_file,"host_and_group.conf")
    config=configparser.ConfigParser()
    config.read(host_path)

    #sections=config.sections()
    #option=config.options("default")

    exec_host_info=[]
    kvs=config.items("default")

    #str_val=config.get("web","web2")
    #int_val=config.getint("db","db_master")
    #print(sections)
    #print(option)
    print(template.GROUP_MENU.format("default"),end="")
    common.show_message("HOSTNAME:\t\t\tIP:","WARN")
    #print(kvs)

    for i in kvs:
        exec_host_info.append(i[1].split())
        common.show_message("{0}\t\t\t\t\t{1}".format(i[0],i[1].split()[0]),"INFO")
    return exec_host_info
    # print("\t{0}\t\t\t{1}".format(kvs[0][0],kvs[0][1]))
    # print(str_val)
    #print(int_val)
    #print(exec_host_info)

#load_default_host()


def load_host_by_name(groupname):
    '''
    通过指定组名，加载组内的信息
    :param groupname: 组名
    :return: 组内信息
    '''
    host_path=os.path.join(settings.db_file,"host_and_group.conf")
    config=configparser.ConfigParser()
    config.read(host_path)
    try:
        exec_host_info=[]
        kvs=config.items(groupname)
        print(template.GROUP_MENU.format(groupname),end="")
        common.show_message("HOSTNAME:\t\t\tIP:","WARN")
        for i in kvs:
            common.show_message("{0}\t\t\t\t{1}".format(i[0],i[1].split()[0]),"INFO")
            exec_host_info.append(i[1].split())
        #print(exec_host_info)
        return exec_host_info
    except configparser.NoSectionError as e:
        common.show_message(exec_code["202"].format(groupname),"ERR")
        exec_log.error(exec_code["202"].format(groupname))




#load_host_by_name("web")









