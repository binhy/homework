#!/usr/bin/python
#coding=utf-8
'''
这个登陆接口是我一开始想到的，比较low，用户随便输，密码固死是123
'''

username_msg="please input your username:"
passwd_msg="please input your passwd:"
username=raw_input(username_msg)
lock_user_list=[]

count=0
with open('lock_user.txt') as f:  #判断用户是否被锁
    for i in f:
        lock_user_list.append(i.strip())
while count < 3:                     #3次循环
    if username in lock_user_list:   #如果在锁列表，则退出
        print "your already lock:%s" %username
        break
    else:
        passwd=raw_input(passwd_msg) #不是锁用户，进入输入密码
        if passwd == "123":         #密码正确
            print "your login sucess:%s" %username #登陆成功
            break
        else:
            count +=1                #密码输错，count+1，进入下次循环
            continue
else:
    print("Too many retrys and your lock:%s !") %(username) #输错3次密码，打印已被锁的信息
    lock_file=open("lock_user.txt","a")
    print >> lock_file,username #把输错3次密码的用户追加到锁文件
    lock_file.close() #关闭锁文件

