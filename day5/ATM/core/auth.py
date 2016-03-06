#!/usr/bin/env python
#coding=utf-8

import os
from core import db_handler
from conf import settings
from core import logger
import json
import time


def acc_login(user_data,log_obj):
    retry_count=0
    while user_data['is_authenticated'] is not True and retry_count < 3:
        account=input("\033[32;1m请输入您的信用卡帐号：\033[0m").strip()
        password=input("\033[32;1m请输入你的密码：\033[0m").strip()
        auth=acc_auth(account,password)
        if auth:
            user_data['is_authenticated']=True
            user_data['account_id']=account
            return auth
        retry_count +=1
    else:
        log_obj.error("输入太多次错误%s"%account)
        exit()


def acc_auth(account,password):
    db_path=db_handler.db_handler(settings.DATABASE)
    account_file='%s/%s.json'%(db_path,account)
    print(account_file)
    if os.path.isfile(account_file):
        with open(account_file,'r') as f:
            account_data=json.load(f)
            if account_data['password']==password:
                exp_time_stamp=time.mktime(time.strptime(account_data['expire_date'],"%Y-%m-%d"))
                if time.time() > exp_time_stamp:
                    print("\033[31;1m用户已经过期\033[0m")
                else:
                    return account_data
    else:
        print("\033[31;1m用户不存在\033[0m")



