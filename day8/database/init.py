#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import json,sys
import configparser

config=configparser.ConfigParser()

#第一个节段,没有分组的成员
config["DEFAULT"] = {
   'LB1':'192.168.10.3 root 22'
}

#第二个节段，web组
config["web"]={}
config['web']['web7']='192.168.10.6 root 22'
config['web']['web2']='192.168.10.32 root 22'
config['web']['web3']='192.168.10.33 root 22'



#第三个节段，db组
config['db']={}
config['db']['DB_master']='192.168.10.21 root 22'
config['db']['DB_slave']='192.168.10.4 root 22'


with open('host_and_group.conf','w') as f:
    config.write(f)




# dic={
#     'password':'40bd001563085fc35165329ea1ff5c5ecbdbbeef', #123
#     'is_locked':0  #0 not locked ,1 is locked
#     }
# with open('yaobin.json','w') as f:
#     json.dump(dic,f)


# print(sys.modules[__name__])