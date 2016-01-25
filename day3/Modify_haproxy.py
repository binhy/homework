#!/usr/bin/python
#coding=utf-8

import os,sys
import json
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


#查看函数
def view(input_backend):
    backend_title='backend %s' %(input_backend)
    with open(haproxy_file) as f:
        server_list=[]    #定义一个匹配到的后端server列表
        flag=True        #主标记
        for i in f:
            i=i.strip()  #把每行的空白剔除
            if i == backend_title: #匹配到backend标题
                flag=False           #标记变为False
                continue           #暂停循环
            elif not flag and i.startswith("backend"): #如果再次遇到以backend开头的行
                break                      #退出
            elif not flag and i: #如果flag=False 和i有东西
                server_list.append(i) #同时增加到后端server列表
        if server_list:
             pass
        else:
             print "原配置文件%s不存在:%s后端!" %(haproxy_file,input_backend)
    return server_list #返回server列表





#增加函数
def add_backend(add_str):
    read_dict=json.loads(add_str)                              #Json格式字符串解码转换成Python对象，这里是字符串转为字典。
    backend_title = "backend %s" %(read_dict['backend'])   #获取你输入的backend名称
    record_list=view(read_dict['backend'])          #获取是否已经存在这个backend的记录,返回的是server列表
    add_server="server %s weight %d maxconn %d" %(read_dict['record']['server'],read_dict['record']['weight'],read_dict['record']['maxconn']) #你输入的想增加的backend记录，格式化成字符串
    if not record_list:                             #如果你输入的backend是不存在的
        print("您输入的这个:%s后端会帮你创建！") %(read_dict['backend'])
        record_list.append(backend_title)            #增加backend标题到server列表
        record_list.append(add_server)               #增加你输入的server到server列表
        with open(haproxy_file) as read_file,open(haproxy_file_new,"w") as write_file: #打开一个读文件和一个写文件
            for line in read_file:                  #循环读文件
                write_file.write(line)               #把全部都写入写文件
            for i in record_list:                   #最后循环serverlist，把新增的内容加到文件末尾
                if i.startswith("backend"):        #如果以backend开头
                    write_file.write(i+"\n")        #写标题进去
                else:                               #如果不是，就是写server的记录进去
                    write_file.write("%s%s\n"%(8*" ",i))       #8个空格+server记录
    else:                                           #else ，就是说你输入的backend本身存在
        record_list.insert(0,backend_title)          #如果backend已经存在，server列表第一项增加一个backend的标题
        if add_server not in record_list:           #判断你输入的server是否已经本身存在
            record_list.append(add_server)           #不存在就增加到server列表
        with open(haproxy_file) as read_file,open(haproxy_file_new,"w") as write_file:  #打开一个读文件和一个写文件
            flag=True                             #是否写入new文件的标记，开始为True，这里是True才写入！请往下面看！
            write_backend_record=True             #写backend记录到new文件的标志，True才写。
            for line in read_file:                #循环读文件
                line_strip=line.strip()            #去取每行的两边空白
                if line_strip==backend_title:      #如果匹配到backend的标题
                    flag=False                     #写入new文件的标记变为False
                    continue                     #暂停这次循环
                elif flag and line:              #new文件标记为True和line有东西，才写内容进去new文件
                    write_file.write(line)        #写入new文件
                elif not flag and line_strip.startswith("backend"):   #new文件标记为False和行是以backend开头
                    flag=True                                            #new文件标记马上变为True,以确保下次循环的内容继续写入new文件
                    write_file.write(line)                               #马上把匹配到的backend标题写入new文件
                else:
                    if write_backend_record:                 #如果write_backend_record 标志为True，进去下面的循环
                        for i in record_list:               #循环server列表
                            if i.startswith("backend"):   #如果以backend开头
                                write_file.write(i+'\n')   #写backend标题进去
                            else:                           #如果不是，就是写server的记录进去
                                write_file.write("%s%s\n"%(8*" ",i))    #8个空格+server记录
                    write_backend_record=False       #这里为什么要False呢？因为下一次循环是到原来文件的server记录，上面3个if条件都不匹配，最后来到else，我已经在上一次循环写进去new文件了，所以不需要重复再写！所以标记变为False
    os.rename(haproxy_file,haproxy_file_bak)
    os.rename(haproxy_file_new,haproxy_file)


#删除函数
def del_backend(del_str):
    read_dict=json.loads(del_str)                             #Json格式字符串解码转换成Python对象，这里是字符串转为字典。
    backend_title = "backend %s" %(read_dict['backend'])  #获取你输入的backend名称
    record_list=view(read_dict['backend'])                  #获取是否已经存在这个backend的记录,返回的是server列表
    del_server="server %s weight %d maxconn %d" %(read_dict['record']['server'],read_dict['record']['weight'],read_dict['record']['maxconn'])  #你输入的想删除的backend记录，格式化成字符串
    if not record_list: #如果你想删除的连backend本身都不存在
        return          #退出
    else:               #获取的server列表有数据，哪怕是一条
        if del_server in record_list:        #如果你想删除的server在server列表里面
            record_list.remove(del_server)    #就删除这条数据
            if len(record_list) > 0:         #如果最后server列表数据大于0条
                record_list.insert(0,backend_title)     #在server列表的第一项增加backend标题
        else:           #如果你想删除的server不在server列表里面
            print("backend:%s,不存在你想删除的记录:%s") %(read_dict['backend'],del_server)
            return      #退出

        with open(haproxy_file) as read_file,open(haproxy_file_new,"w") as write_file: #打开一个读文件和一个写文件
            flag=True                                                     #是否写入new文件的标记，开始为True，这里是True才写入！请往下面看！
            write_backend_record=True                                     #写backend记录到new文件的标志，True才写。
            for i in read_file:                                          #循环读文件
                line_strip=i.strip()                                      #去取每行的两边空白
                if line_strip==backend_title:                             #如果匹配到backend的标题
                    flag=False                                             #写入new文件的标记变为False
                    continue                                              #暂停这次循环
                elif flag and i:                                          #new文件标记为True和line有东西，才写内容进去new文件
                    write_file.write(i)                                    #写入new文件
                elif not flag and i.startswith("backend"):             #new文件标记为False和行是以backend开头
                    flag=True                                             #new文件标记马上变为True,以确保下次循环的内容继续写入new文件
                    write_file.write(i)                                    #马上把匹配到的backend标题写入new文件
                else:
                    if write_backend_record:                              #如果write_backend_record 标志为True，进去下面的循环
                        for i in record_list:                            #循环server列表
                            if i.startswith("backend"):                 #如果以backend开头
                                write_file.write(i+"\n")                 #写backend标题进去
                            else:                                        #如果不是，就是写server的记录进去
                                write_file.write("%s%s\n"%(8*" ",i))    #8个空格+server记录
                        write_backend_record=False   #这里为什么要False呢？因为下一次循环是到原来文件的server记录，上面3个if条件都不匹配，最后来到else，我已经在上一次循环写进去new文件了，所以不需要重复再写！所以标记变为False
    os.rename(haproxy_file,haproxy_file_bak)
    os.rename(haproxy_file_new,haproxy_file)








#主循环
if __name__ == "__main__":
    now=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H:%M:%S')
    haproxy_file='haproxy.cfg'
    haproxy_file_bak='haproxy.cfg_bak_%s'%(now)
    haproxy_file_new="haproxy.cfg.new"
    while True:
        print ('''
        ###############################################
        #           ❤欢迎进入修改haproxy.cfg❤        #
        #            您有以下选择：                    #
        #            (1): 查看backend记录             #
        #            (2): 增加backend记录             #
        #            (3): 删除backend记录             #
        #            (q): 退出                        #
        ###############################################
        ''')
        init_your_choice=raw_input("please choice your like record and do somthing:")
        record_list=["1","2","3","4","q"]
        if init_your_choice not in record_list:
            print("输入错误，请重新输入！")
            continue
        if init_your_choice == "1":
            input_backend=raw_input("please choice your like backend:")
            server_list=view(input_backend)
            if server_list:
                print("[[%s backend的server记录是：]]") %(input_backend)
            for i in server_list:
                print("%s") %(i)
        elif init_your_choice == "2":
            new_backend=raw_input('请输入要新增加的记录:')
            add_backend(new_backend)
        elif init_your_choice == "3":
            remove_backend=raw_input("请输入要删除的记录:")
            del_backend(remove_backend)
        elif init_your_choice == "q":
            print("good bye!!!!")
            sys.exit()

















