#!/usr/bin/env python
#coding=utf-8

import sys,os
import logging

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#D:\Users\bin\PycharmProjects\s12\homework\day5\atm
#sys.path.append(BASE_DIR)
#print(BASE_DIR)
#print(sys.path)


DATABASE={
    'engine':'file_storage',
    'name':'accounts',
    'path':"%s/db" %BASE_DIR
}


LOG_LEVEL=logging.INFO  #日志水平
#日志类型
LOG_TYPES={
    'transaction': 'transactions.log',
    'access': 'access.log',
}


#交易类型
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},  #还款
    'withdraw':{'action':'minus', 'interest':0.05},  #提现
    'transfer':{'action':'minus', 'interest':0.05},  #转让
    'consume':{'action':'minus', 'interest':0},      #消费

}