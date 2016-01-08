#!/usr/bin/python
#coding=utf-8
'''
实现根据帐号密码文件account.txt的登陆判断！
'''

username_msg="please input your username:"
passwd_msg="please input your passwd:"
username=raw_input(username_msg)
account_dict={} #定义一个空的帐号密码字典
lock_user_list=[] #定义一个空的锁用户列表

##初始化帐号密码文件，生成一个帐号密码字典
def account_passwd_dict():
    with open('account.txt') as f:
        account_passwd=f.readlines()
        for i in account_passwd:
            account_dict[i.split()[0]]=i.split()[1]
    #print account_dict

##初始化锁定用户文件，生成一个已被锁用户列表
def lock_list():
    with open('lock_user.txt') as f:
        for i in f:
            lock_user_list.append(i.strip())
    #print lock_user_list

##开始循环
def go():
    count=0
    while count < 3:
        if username in lock_user_list:    #判断用户是否被锁
            print "your already lock:%s" %username
            break
        else:
            if username in account_dict:  #判断是否有这个用户
                passwd=raw_input(passwd_msg)  #有这个用户，那么请输入密码
                if passwd == account_dict[username]:  #判断密码是否正确
                    print "your login sucess:%s" %username
                    break
                else:
                    count +=1              #密码不正确，可以重输3次
                    continue
            else:
                 print "username:%s is not exsit!" %(username) #打印帐号不存在
                 break   #没有这个用户，就break，退出循环

    else:
        print("Too many retrys and your lock:%s !") %(username) #打印输错3次密码，并且锁定该用户
        lock_file=open("lock_user.txt","a")
        print >> lock_file,username #追加用户到锁文件
        lock_file.close() #关闭锁文件

if __name__ == '__main__':
    account_passwd_dict()
    lock_list()
    go()

