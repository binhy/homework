#!/usr/bin/python
#coding=utf-8


from conf import settings
from modules import logger,common
from modules.User import User
from dbhelper import dbapi
import time,json,os,shutil
import socketserver
import subprocess

ftpserver_logger=logger.logger("server_ftp")

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        ftpserver_logger.info("client {0} connected".format(self.client_address))
        #发送一个连接成功标示
        self.request.send(bytes("conn_succ","utf8"))
        while True:
            data=self.request.recv(1024)
            print("---data:",data)
            if not data:
                common.show_message("Has lost client: {0}".format(self.client_address),'ERROR')
                break
            self.instruction_allowcation(data)



    def instruction_allowcation(self,instructions):
        '''
        功能分发器,负责按照客户端的指令分配给相应的函数处理
        :param instructions:
        :return:
        '''
        instructions=str(instructions,'utf8').split("|")
        function_str = instructions[0]
        if hasattr(self,function_str):
            func=getattr(self,function_str)
            func(instructions)


    def get(self,data):
        '''
        下载文件
        :param data: ['get',xxx]
        :return:
        '''
        if self.user_inst.exists:
            want_file=data[1]   #获取你想要下载的文件
            file_abs_path=os.path.join(self.user_inst.currpath,want_file)  #合并成一个对应用户文件的绝对路径
            if os.path.isfile(file_abs_path):        #如果是文件
                file_size=os.path.getsize(file_abs_path)   #文件大小
                file_md5=common.encry_md5(file_abs_path)    #文件md5
                return_data="respon|file_exists|{0}|{1}".format(file_size,file_md5)  #合并信息"respon|file_exists|file_size|file_md5"
                self.request.send(bytes(return_data,"utf8"))                             #回合并消息给客户端


                if str(self.request.recv(1024),"utf8") == "703": #如果客户端说准备好接受
                    common.show_message("start transfer file: {0} ......".format(file_abs_path),"NOTICE")
                    send_size=0
                    t_start=time.time()
                    with open(file_abs_path,'rb') as f:  #开始传送！
                        while file_size != send_size:
                            data=f.read(4096)
                            self.request.send(data)
                            send_size+=len(data)
                            #common.show_message("send:{0} {1}".format(file_size,send_size))
                        else:
                            c_time=time.time() - t_start
                            ftpserver_logger.info("----file:{0} transfer finish! and transfer time: {1}---".format(file_abs_path,c_time))
                            common.show_message("----file:{0} transfer finish! and transfer time: {1}---".format(file_abs_path,c_time),"NOTICE")
            elif os.path.isdir(file_abs_path):  #是一个目录
                return_data="respon|{0}".format(704)
                self.request.send(bytes(return_data,"utf8"))
            else:                               #文件不存在
                return_data="respon|{0}".format(701)
                self.request.send(bytes(return_data,"utf8"))
        else:
            return_data="respon|{0}".format(600)     #还没登陆
            self.request.send(bytes(return_data,"utf8"))
            #common.show_message("you are not exists!not allow get file!!","ERROR")



    def put(self,data):
        '''
        上传方法，只支持绝对路径
        :param data: ['put',xxx,'file_size','file_md5']
        :return:
        '''
        if self.user_inst.exists:  #如果已经登录
            want_file=data[1]  #因为客户端已经验证了想上传的文件存在，那么这里是绝对路径文件
            free_spaced=self.user_inst.quotation - self.user_inst.usedspace  #用户剩余空间
            want_file_spaced=os.path.getsize(want_file)/1024/1024  #获取你想上传的文件的大小，单位MB
            if free_spaced > want_file_spaced: #表示用户空间足够上传文件
                file_size=int(data[2])
                file_md5=data[3]
                self.request.send(bytes("respon|{0}".format(203),"utf8"))  #发送一个标示，表示磁盘空间足够,并且准备接收

                put_file_path=os.path.join(self.user_inst.currpath,os.path.basename(want_file))  #合并server端的上传文件路径

                recv_size=0
                with open(put_file_path,'wb') as f:  #打开文件
                    while file_size!=recv_size:
                        data=self.request.recv(4096)
                        recv_size+=len(data)
                        f.write(data)
                    else:
                        self.user_inst.update_usedspace(self.user_inst.username)  #接收完文件，更新用户磁盘空间
                        self.request.send(bytes(str(self.user_inst.usedspace),'utf8'))   #发送一个最新的usedspace空间回去给客户端
                        ftpserver_logger.info("----file:{0}  put finished-----".format(want_file))
                        common.show_message("----file:{0} put finished-----".format(want_file),"NOTICE")

                #md5 验证
                check_md5=common.encry_md5(put_file_path)
                if check_md5 == file_md5:
                    ftpserver_logger.critical("file:{0} md5 verification  succ!!".format(put_file_path))
                    common.show_message("file:{0} md5 verification  succ!!".format(put_file_path),"INFO")
                else:
                    ftpserver_logger.info('file:{0} md5 verification not succ!!'.format(put_file_path))
                    common.show_message('file:{0} md5 verification not succ!!'.format(put_file_path),"INFO" )

            else:
                return_data="respon|{0}".format(800)  #表示不够空间
                self.request.send(bytes(return_data,"utf8"))

        else:
            return_data="respon|{0}".format(600)     #还没登陆
            self.request.send(bytes(return_data,"utf8"))


    def rmf(self,data):
        '''
        删除文件方法
        :param data: ['rmf','xxx']，xxx是相对路径
        :return:
        '''
        rm_file=os.path.join(self.user_inst.currpath,data[1]) #合并当前目录路径+文件名
        if os.path.isfile(rm_file): #有这个文件
            os.remove(rm_file)  #删除文件
            self.user_inst.update_usedspace(self.user_inst.username)  #删除完文件，更新用户磁盘空间
            return_data="respon|{0}|{1}".format(204,self.user_inst.usedspace)
            ftpserver_logger.info("remove file:{0} succ".format(rm_file))
        elif os.path.isdir(rm_file):  #这是一个目录
            return_data="respon|{0}".format(704)
            ftpserver_logger.warn("want to remove file:{0} but this file is dir !!!".format(rm_file))
        else:                       #不存在这个文件
            return_data= "respno|{0}".format(701)
            ftpserver_logger.warn("want to remove file:{0} but this file is not exists!!!".format(rm_file))

        self.request.send(bytes(return_data,'utf8')) #回一个消息给客户端，告诉删除文件是否成功




    def rmd(self,data):
        '''
        删除目录方法
        :param data: ['rmd','xxx'] ，xxx是相对路径
        :return:
        '''
        rm_dir=os.path.join(self.user_inst.currpath,data[1]) #合并当前目录路径+目录
        if os.path.isdir(rm_dir): #有这个目录
            shutil.rmtree(rm_dir)  #删除目录
            self.user_inst.update_usedspace(self.user_inst.username)  #删除完目录，更新用户磁盘空间
            return_data="respon|{0}|{1}".format(205,self.user_inst.usedspace)
            ftpserver_logger.info("remove dir:{0} succ".format(rm_dir))
        elif os.path.isfile(rm_dir):  #这是一个文件
            return_data="respon|{0}".format(705)
            ftpserver_logger.warn("want to remove dir:{0} but this dir is file !!!".format(rm_dir))
        else:                       #不存在这个目录
            return_data= "respno|{0}".format(1001)
            ftpserver_logger.warn("want to remove dir:{0} but this dir is not exists!!!".format(rm_dir))

        self.request.send(bytes(return_data,'utf8')) #回一个消息给客户端，告诉删除目录是否成功

    def cd(self,data):
        '''
        cd 方法
        :param data: ['cd','xxx']
        :return: "xxx|xxx"
        '''
        cd_foler=data[1]  #获取你想进入的目录


        try:
            if cd_foler=="..":  #如果是 cd ..
                #print("dfdsfdsfdsafd .......")
                if self.user_inst.currpath == self.user_inst.homepath:  #如果已经在家目录了
                    return_data="alreay_in_homepath|{0}".format(self.user_inst.homepath)
                else:                                                    #不是在家目录
                    self.user_inst.currpath = os.path.dirname(self.user_inst.currpath)  #改变当前的currpath
                    return_data="backspace_succ|{0}".format(self.user_inst.currpath)
            else:
                tmp_path=os.path.join(self.user_inst.currpath,cd_foler)  #组合你想去到的path
                if os.path.isdir(tmp_path):                             #判断是不是目录
                    self.user_inst.currpath=tmp_path                    #是就改变当前的currpath
                    return_data="succ_cd_path|{0}".format(self.user_inst.currpath)
                else:                                                  #不是目录
                    return_data="isn't_dir|{0}".format(tmp_path)
            self.request.send(bytes(return_data,'utf8'))               #回消息给客户端
        except Exception as e:
            ftpserver_logger.error(e)





    def ls(self,data):
        '''
        ls方法
        :param data: ['ls','|']
        :return:
        '''
        #print(data)
        ls_info=data[0]+" -l"  #取列表第一个ls
        ls_cmd="{0} {1}".format(ls_info,self.user_inst.currpath)  #合并 ls -l + 当前用户所在的目录
        #print(ls_cmd)
        cmd_call = subprocess.Popen(ls_cmd,shell=True,stdout=subprocess.PIPE)  #执行命令
        cmd_result=cmd_call.stdout.read()  #获取执行命令的结果

        if len(cmd_result) == 0: #如果执行没有结果
            cmd_result=b'cmd excution has not output...'  #定义....not output的消息
        ack_msg=bytes("CMD_RESULT_SIZE {0}".format(len(cmd_result)),'utf8')  #合并消息CDM_RESULT_SIZE XXX
        self.request.send(ack_msg)  #发送一个合并消息CMD_RESULT_SIZE XXX 给客户端
        client_ack=self.request.recv(50)  #如果这时不等客户端确认就立刻给客户端发文件内容，因为为了减少IO操作，socket发送和接收是有缓冲区的，缓冲区满了才会发送，那上一条消息很有可能会和文件内容的一部分被合并成一条消息发给客户端，这就行成了粘包，所以这里等待客户端的一个确认消息，就把两次发送分开了，不会再有粘包
        if client_ack.decode() == 'CLIENT_READY_TO_RECV':  #客户端准备好接受
            self.request.send(cmd_result)  #把执行结果发过去给客户端





    def user_auth(self,data):
        '''
        服务端用户密码认证方法
        :param data: [user_auth,{"password": "xxx", "username": "xxx"}]
        :return:
        '''
        auth_info=json.loads(data[1])
        user=auth_info['username']
        password=auth_info['password']

        user_space=None
        self.user_inst=User(user)  #服务端这里认证成功的话，就会实例化user

        if self.user_inst.exists:             #用户存在
            if self.user_inst.auth_pass(password):  #用户密码认证
                self.login_user=user           #定义一个登陆了的user
                user_space = "{0}|{1}".format(self.user_inst.quotation,self.user_inst.usedspace) #用户空间限额+已用空间
                respons_code=201  #认证成功
            else:
                respons_code=601  #密码错误
                common.show_message('invalid password!','ERROR')
                ftpserver_logger.error("invalid password!")
        else:
            respons_code = 600 #用户不存在
            common.show_message('invalid username: {0}'.format(user),'ERROR')
            ftpserver_logger.error("invalid username",user)

        # 认证结果发送给客户端
        respon_str="respon|{0}|{1}".format(respons_code,user_space)
        self.request.send(bytes(respon_str,'utf-8'))  #发送#"respon|code|user_space" 过去给客户端

