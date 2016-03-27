#!/usr/bin/python
#coding=utf-8

import os,sys
import subprocess


BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# import json
# import hashlib
# def encry_sha(string):
#     sha=hashlib.sha224()
#     sha.update(string.encode())
#     sha_value=sha.hexdigest()
#     return sha_value
#
#
#
# dic={'yaobin':{'password':'78d8045d684abd2eece923758f3cd781489df3a48e1278982466017f',
#         'quotation': 500, #500M
#         'usedspace':0,
#         'expire': '2016-08-22',
#         'is_lock':0
#         },
#
#     'test':{'password':'e7bedacebad77e3bc61d1e27db602019c6e0fc954d6c856bd2719968',
#     'quotation': 1000, #1G
#     'usedspace':0,
#     'expire': '2016-08-22',
#     'is_lock':0
#         },
#      }
#
#
# print(json.dumps(dic))

# a=encry_sha("456")
# print(a)
# username="yaobin"
# USER_HOME_FOLDER=os.path.join(BASE_DIR,"uploads")
# print(USER_HOME_FOLDER)
# user_path=os.path.join(USER_HOME_FOLDER,username)
# print(user_path)
# ls_cmd="ls {0}".format(user_path)
# print(ls_cmd)
# cmd_call = subprocess.Popen(ls_cmd,shell=True,stdout=subprocess.PIPE)
# cmd_result=cmd_call.stdout.read()
# print(cmd_result)

# a="ls"
# print(len(a))

# import os,sys,string
# import time
#
# def view_bar(num=1, sum=100, bar_word=":"):
#     rate = float(num) / float(sum)
#     rate_num = int(rate * 100)
#     print('\r%d%% :' %(rate_num),end='\r')
#     for i in range(0, num):
#         os.write(1,)
#     sys.stdout.flush()
#
# if __name__ == '__main__':
#     for i in range(0, 100):
#         time.sleep(0.1)
#         view_bar(i, 100)

# a=os.path('D:/pycharm_project/s12/homework/day7')
# print(a)

# def GetPathSize():
#     # Totalsize=0
#     # for strRoot,lsDir,lsFiles in os.walk
#     from os.path import join, getsize
#     size=0
#     for root, dirs, files in os.walk('D:/pycharm_project/s12/homework/day7/server'):
#         #print(root, "consumes", end="")
#         print(root,dirs,files)
#         #print(sum([getsize(join(root, name)) for name in files]), end="")
#         size+=sum([getsize(join(root, name)) for name in files])
#         #print("bytes in", len(files), "non-directory files")
#     print(size)
#     print(type(size))
#
# GetPathSize()