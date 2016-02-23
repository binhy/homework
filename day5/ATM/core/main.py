#!/usr/bin/env python
#coding=utf-8

from core import accounts
from core import auth
from core import db_handler
from core import logger
from core import transaction
import time

trans_logger=logger.logger('transaction')
access_logger=logger.logger('access')




user_data = {
    'account_id':None,
    'is_authenticated':False,
    'account_data':None
}

#打印帐号信息
def account_info(acc_data):
    print(user_data)

#还款
def repay(acc_data):
    account_data=accounts.load_current_balance(acc_data['account_id'])
    current_balance='''--------信用卡信息---------
    信用额度：%s
    金额：%s
    ''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag=True
    while back_flag:
        repay_amount=input("\033[33;1m请输入你还款的金额:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance=transaction.make_transaction(trans_logger,account_data,'还款',repay_amount)
            if new_balance:
                print('''\033[42;1m新的金额:%s\033[0m''' %(new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)

        if repay_amount =="b":
            back_flag=False




#取款
def withraw(acc_data):
    account_data=accounts.load_current_balance(acc_data['account_id'])
    current_balance='''-----信用卡信息-----
    信用额度：%s
    金额：%s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag=True
    while back_flag:
        withraw_amount=input("\033[33;1m请输入取款金额:\033[0m")
        if len(withraw_amount) > 0 and withraw_amount.isdigit():
            new_balance=transaction.make_transaction(trans_logger,account_data,'取款',withraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

        if withraw_amount=='b':
            back_flag=True

#转账
def transfer(acc_data):
    pass

#账单
def pay_check(acc_data):
    pass

#退出
def logout(acc_data):
    pass


def interactive(acc_data):
    menu=u'''
    \033[32;1m------nimei bank-----
    1.账户信息
    2.还款
    3.取款
    4.转账
    5.退出
\033[0m
    '''
    menu_dic={
        '1':account_info,
        '2':repay,
        '3':withraw,
        '4':transfer,
        '5':pay_check,
        '6':logout
    }

    exit_flag=True
    while exit:
        print(menu)
        user_option=input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    acc_data=auth.acc_login(user_data,access_logger)
    if user_data['is_authenticated']:
        user_data['account_data']=acc_data
        interactive(user_data)


