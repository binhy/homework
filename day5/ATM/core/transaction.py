#!/usr/bin/env python
#coding=utf-8

from conf import settings
from core import accounts
from core import logger

def make_transaction(log_obj,account_data,tran_type,amount,**kwargs):
    amount=float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        interest=amount*settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance=account_data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance=old_balance+amount+interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance=old_balance-amount-interest
            if new_balance<0:
                print('''你的信用额度为[%s],不足够取现交易[-%s],你当前的金额为：[%s]'''
                      %(account_data['credit'],(amount+interest),old_balance))
                return

        account_data['balance']=new_balance
        accounts.dump_account(account_data)
        log_obj.info("账户:%s,动作:%s,交易类型:%s,金额:%s,利息:%s"%(account_data['id'],tran_type,amount,interest))
        return account_data
    else:
        print("\033[31;1m交易类型 [%s] 不存在!\033[0m" % tran_type)

