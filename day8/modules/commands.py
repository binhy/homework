#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

from conf import settings
from conf.code import exec_code
#from modules.myexception import MyException
from modules import logger,common
from dbhelper import dbapi
import os,paramiko
from multiprocessing import Pool


exec_log=logger.logger("exec_log","exec_log.txt")

class exec(object):
    def __init__(self,command_str):
        self.__command__=["show","cmd","sftp"]

        self.command_str=command_str
        self.command_list=self.command_str.split()
        self.command=self.command_list[0]
        if hasattr(self,self.command):
                func=getattr(self,self.command)
                func(self.command_list)
        else:
                 common.show_message(exec_code["200"].format(self.command_str),"CRI")
                 exec_log.error(exec_code["200"].format(self.command_str))

    def verify_command(func):
        def inner(self,command_list):
            try:
                if self.command=="list":
                    if len(command_list) == 2 and command_list[1] =="-a":  #list -a
                        pass
                    elif len(command_list) == 3 and command_list[1] == "-G": #list -G xxx
                        pass
                    else:
                            common.show_message(exec_code["201"].format(" ".join(command_list)),"WARN")
                            exec_log.error(exec_code["201"].format(" ".join(command_list)))
                            return

                elif self.command=="cmd":
                    if len(command_list) == 4 and command_list[2] == "-c": #cmd hostname -c xxx
                        pass
                    elif len(command_list) == 5 and command_list[1] == "-G" and command_list[3] =="-c": #cmd -G groupname -c xxx
                        pass
                    else:
                        common.show_message(exec_code["203"].format(" ".join((command_list))),"WARN")
                        exec_log.error(exec_code["203"].format(" ".join(command_list)))
                        return

                elif self.command=="sftp":
                    pass

            except Exception as e:
                exec_log.error(e)

            return func(self,command_list)
        return inner

    @verify_command
    def list(self,command_list):
        if command_list[1] == "-a": #list -a
            dbapi.load_default_host()
        elif command_list[1] == "-G": # list -G xxx
            group_name=command_list[2]
            dbapi.load_host_by_name(group_name)

    @verify_command
    def cmd(self,command_list):
        if command_list[1]=="-G": #cmd -G groupname -c xxx
            exec_command=command_list[4]  #要执行的命令
            group_name=command_list[2]    #组名
            exec_host_info=dbapi.load_host_by_name(group_name) #执行host信息，例如：[['192.168.10.6', 'root', '22'], ['192.168.10.32', 'root', '22'], ['192.168.10.33', 'root', '22']]

            pool=Pool(5)  #开启进程池执行服务器操作
            for host_info in exec_host_info:
                print(host_info)
                print(exec_command)
                pool.apply_async(self._ssh_exec_cmd,args=(host_info,exec_command))

            pool.close()
            pool.join()

        else:           #cmd hostname -c xxx
            pass

    def _ssh_exec_cmd(self,host_info,exec_command):
        '''
        paramiko 执行命令方法
        :param host_info: 主机信息列表
        :param exec_command:  执行的命令
        :return:
        '''
        ip=host_info[0]
        user=host_info[1]
        port=int(host_info[2])


        try:
            transport = paramiko.Transport((ip,port))

            privatekeyfile=os.path.join(settings.rsa_file_path,"id_rsa")
            print(privatekeyfile)
            my_key=paramiko.RSAKey.from_private_key(privatekeyfile)
            print(privatekeyfile)
            transport.connect(username=user,pkey=my_key)

            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh._transport=transport
            stdin,stdout,stderr = ssh.exec_command(command=exec_command)

            common.show_message("ip:{0} result:".format(ip),'INFO')
            cmd_result=stdout.read(),stderr.read()
            for line in cmd_result:
                print(str(line,'utf8'))

            transport.close()
        except Exception as e:
            print(e)
            exec_log.error(e)



    @verify_command
    def sftp(self,command_list):
        print("main sftp...")


