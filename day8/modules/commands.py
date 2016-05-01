#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

from conf import settings
from conf.code import exec_code
from modules import logger,common
from dbhelper import dbapi
import os,paramiko
from multiprocessing import Pool


exec_log=logger.logger("exec_log","exec_log.txt")

class exec(object):
    def __init__(self,command_str):
        self.command_str=command_str  #您输入的字符
        self.command_list=self.command_str.split() #您输入的字符分割列表
        try:
            self.command=self.command_list[0]  #获取你第一个输入的命令，你第一个命令只能是list,cmd,sftp,q/quit
            if hasattr(self,self.command):   #反射进入下面的list,cmd,sftp方法
                func=getattr(self,self.command)
                func(self.command_list)     #把您输入的字符分割列表self.command_list当作形式参数传进去下面的list,cmd,sftp方法
            else:
                common.show_message(exec_code["200"].format(self.command_str),"CRI")
                exec_log.error(exec_code["200"].format(self.command_str))
        except IndexError as e:
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
                    if len(command_list) ==5 and command_list[1] == "-g" and command_list[3] == "-c": #cmd -g hostname -c xxx or cmd -g hostname1,hostname2 -c "xxx xxx"
                        pass
                    elif len(command_list) ==5 and command_list[1] == "-G" and command_list[3] =="-c": #cmd -G groupname -c xxx or cmd -G groupname1,groupname2 -c "xxx xxx"
                        pass
                    else:
                        common.show_message(exec_code["203"].format(" ".join((command_list))),"WARN")
                        exec_log.error(exec_code["203"].format(" ".join(command_list)))
                        return

                elif self.command=="sftp":
                    if len(command_list) == 8 and command_list[1] =="-g" and command_list[3] == "-u" and command_list[4]=="-s" and command_list[6] =="-t": #hostname 上传
                        #例子：sftp -g web2 -u -s /tmp/test.txt -t /tmp/test.txt
                        if os.path.exists(command_list[5]): #判断上传文件存不存在
                            pass
                        else:
                            common.show_message(exec_code["206"].format(command_list[5]),"WARN")
                            exec_log.error(exec_code["206"].format(command_list[5]))
                            return
                    elif len(command_list) == 8 and command_list[1] =="-G" and command_list[3] == "-u" and command_list[4]=="-s" and command_list[6] =="-t": #groupname 上传
                        #例子： sftp -G web -u -s /tmp/test.txt -t /tmp/test.txt
                        if os.path.exists(command_list[5]):  #判断上传文件存不存在
                            pass
                        else:
                            common.show_message(exec_code["206"].format(command_list[5]),"WARN")
                            exec_log.error(exec_code["206"].format(command_list[5]))
                            return

                    elif len(command_list) == 8 and command_list[1] =="-g" and command_list[3] == "-d" and command_list[4]=="-s" and command_list[6] =="-t": #hostname 下载
                        #例子：sftp -g web2 -d -s /tmp/test.txt -t /tmp/test.txt
                        if os.path.exists(os.path.dirname(command_list[7])): #判断下载文件所在的目录存不存在
                            pass
                        else:
                            common.show_message(exec_code["207"].format(os.path.dirname(command_list[7])),"WARN")
                            exec_log.error(exec_code["207"].format(os.path.dirname(command_list[7])))
                            return
                    elif len(command_list) == 8 and command_list[1] =="-G" and command_list[3] == "-d" and command_list[4]=="-s" and command_list[6] =="-t": #groupname 下载
                        #例子：sftp -G web -d -s /tmp/test.txt -t /tmp/test.txt
                         if os.path.exists(os.path.dirname(command_list[7])): #判断下载文件所在的目录存不存在
                            pass
                         else:
                            common.show_message(exec_code["207"].format(os.path.dirname(command_list[7])),"WARN")
                            exec_log.error(exec_code["207"].format(os.path.dirname(command_list[7])))
                            return

                    else:
                        common.show_message(exec_code["205"].format(" ".join((command_list))),"WARN")
                        exec_log.error(exec_code["205"].format(" ".join(command_list)))
                        return
            except Exception as e:
                exec_log.error(e)
            return func(self,command_list)
        return inner

    @verify_command
    def list(self,command_list):
        '''
        list 方法
        :param command_list: 你输入的命令列表
        :return:
        '''
        if command_list[1] == "-a": #list -a
            dbapi.load_default_host()
        elif command_list[1] == "-G": # list -G xxx
            group_name=command_list[2]
            dbapi.load_host_by_gname(group_name)

    @verify_command
    def cmd(self,command_list):
        '''
        cmd 执行命令方法
        :param command_list:你输入的命令列表
        :return:
        '''
        if command_list[1]=="-G":   #cmd -G groupname -c xxx or cmd -G groupname1,groupname2 -c "xxx xxx"
            start_index=command_list.index("-c")+1
            end_index=len(command_list)
            tmp=" ".join(command_list[start_index:end_index]) #临时，还没去除前后的双引号要执行的命令
            exec_command=tmp.replace('"','') #去前后的双引号后，获取真正要执行的命令

            start_index=command_list.index("-G")+1
            end_index=command_list.index("-c")
            group_name=" ".join(command_list[start_index:end_index])  #获取要执行的组名

            exec_host_info=dbapi.load_host_by_gname(group_name) #获取组名对应的host信息
            # 例如：{'web2': ['192.168.10.32', 'root', '22'], 'db_master': ['192.168.10.21', 'root', '22'], 'web7': ['192.168.10.6', 'root', '22'], 'db_slave': ['192.168.10.4', 'root', '22'], 'web3': ['192.168.10.33', 'root', '22']}

        else:           #cmd -g hostname -c xxx or cmd -g hostname1,hostname2 -c "xxx xxx"
            start_index=command_list.index("-c")+1
            end_index=len(command_list)
            tmp=" ".join(command_list[start_index:end_index]) #临时，还没去除前后的双引号要执行的命令
            exec_command=tmp.replace('"','') #去前后的双引号后，获取真正要执行的命令

            start_index=command_list.index("-g")+1
            end_index=command_list.index("-c")
            host_name=" ".join(command_list[start_index:end_index])  #获取要执行的hostname


            exec_host_info=dbapi.load_host_by_hname(host_name) #获取hostname对应的host信息
            #例如：{'web2': ['192.168.10.32', 'root', '22'], 'web3': ['192.168.10.33', 'root', '22']}

        try:
            pool=Pool(5)  #开启进程池执行服务器操作
            for hostname in exec_host_info:
                pool.apply_async(self._ssh_exec_cmd,args=(hostname,exec_host_info[hostname],exec_command))
            pool.close()
            pool.join()
        except TypeError as e:
            pass

    def _ssh_exec_cmd(self,host_name,host_info,exec_command):
        '''
        paramiko 执行命令方法
        :param host_name:  主机名
        :param host_info:  主机信息列表
        :param exec_command: 执行的命令
        :return:
        '''
        hostname=host_name
        ip=host_info[0]
        user=host_info[1]
        port=int(host_info[2])

        try:
            transport = paramiko.Transport((ip,port))

            privatekeyfile=os.path.join(settings.rsa_file_path,"id_rsa")
            my_key=paramiko.RSAKey.from_private_key_file(privatekeyfile,password=settings.rsa_file_pass)
            transport.connect(username=user,pkey=my_key)

            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh._transport=transport
            stdin,stdout,stderr = ssh.exec_command(command=exec_command)


            cmd_result=stdout.read(),stderr.read()
            common.show_message("\nHOSTNAME: {0}  IP:{1} RESULT:".format(hostname,ip),'CRI')
            for line in cmd_result:
                print(str(line,'utf8'))

            transport.close()
        except Exception as e:
            print(e)
            exec_log.error(e)



    @verify_command
    def sftp(self,command_list):
        '''
        sftp 上传下载文件方法
        :param command_list: 你输入的命令列表
        :return:
        '''
        if command_list[3] == "-u": #上传
            src_file=command_list[5]
            dst_file=command_list[7]
            exec_type="u"
            if command_list[1] == "-g":    #指定hostname
                start_index=command_list.index("-g")+1
                end_index=command_list.index("-u")
                host_name=" ".join(command_list[start_index:end_index])  #获取要执行的一个或者多个hostname
                exec_host_info=dbapi.load_host_by_hname(host_name) #获取hostname对应的host信息
            elif command_list[1] == "-G":    #指定组名
                start_index=command_list.index("-G")+1
                end_index=command_list.index("-u")
                group_name=" ".join(command_list[start_index:end_index])  #获取要执行的一个或者多个groupname
                exec_host_info=dbapi.load_host_by_gname(group_name) #获取组名对应的host信息


        else:                     #下载
            src_file=command_list[5]
            dst_file=command_list[7]
            exec_type="d"
            if command_list[1] == "-g":    #指定hostname
                start_index=command_list.index("-g")+1
                end_index=command_list.index("-d")
                host_name=" ".join(command_list[start_index:end_index])  #获取要执行的一个或者多个hostname
                exec_host_info=dbapi.load_host_by_hname(host_name) #获取hostname对应的host信息
            elif command_list[1] == "-G":    #指定组名
                start_index=command_list.index("-G")+1
                end_index=command_list.index("-d")
                group_name=" ".join(command_list[start_index:end_index])  #获取要执行的一个或者多个groupname
                exec_host_info=dbapi.load_host_by_gname(group_name) #获取组名对应的host信息

        try:
            pool=Pool(5)  #开启进程池执行服务器操作
            for hostname in exec_host_info:
                pool.apply_async(self._ssh_exec_sftp,args=(hostname,exec_host_info[hostname],src_file,dst_file,exec_type))
            pool.close()
            pool.join()
        except TypeError as e:
            pass





    def _ssh_exec_sftp(self,host_name,host_info,src,dst,exec_type):
        '''
        paramiko 执行文件上传下载
        :param host_name: 主机名
        :param host_info:  主机信息列表
        :param src: 源文件
        :param dst: 目的地文件
        :param exec_type:  执行类型，u or d ,上传或者下载
        :return:
        '''
        hostname=host_name
        ip=host_info[0]
        user=host_info[1]
        port=int(host_info[2])
        src_file=src
        dst_file=dst
        exec_type=exec_type

        try:
            transport = paramiko.Transport((ip,port))

            privatekeyfile=os.path.join(settings.rsa_file_path,"id_rsa")
            my_key=paramiko.RSAKey.from_private_key_file(privatekeyfile,password=settings.rsa_file_pass)
            transport.connect(username=user,pkey=my_key)

            ssh_ftp=paramiko.SFTPClient.from_transport(transport)
            if exec_type == "u": #上传
                common.show_message("upload src_file:{0}  -->>>>>>>> hostname:{1} IP:{2} dst_file:{3}".format(src_file,hostname,ip,dst_file),'CRI')
                ssh_ftp.put(src_file,dst_file)
            else:                #下载
                dst_file="{0}_{1}".format(dst_file,hostname)  #下载文件，后缀加上hostname吧
                common.show_message("download src_file:{0}  -->>>>>>>> hostname:{1} IP:{2} dst_file:{3}".format(src_file,hostname,ip,dst_file),'CRI')
                ssh_ftp.get(src_file,dst_file)

            transport.close()
        except Exception as e:
            print(e)
            exec_log.error(e)



