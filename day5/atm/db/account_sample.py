#!_*_coding:utf-8_*_
#__author__:"Alex Li"


import sys,os
#print(sys.path)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#print(sys.path)

import json
from conf import settings

acc_dic = {
    'id': 789456,
    'password': 'test',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

account_file='%s/%s/%s.json'%(settings.DATABASE['path'],settings.DATABASE['name'],acc_dic['id'])
# print(account_file)


#print(json.dumps(acc_dic))

#
with open(account_file,'w') as f:
    json.dump(acc_dic,f)