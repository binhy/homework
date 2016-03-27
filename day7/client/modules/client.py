#!/usr/bin/python
#coding=utf-8

import socket
import os,sys,json,getpass,time
from conf import settings,codes,template
from modules import common,logger

client_logger=logger.logger("client_log")

class Client(object):
    def __init__(self,sys_argv):
        '''
        初始化方法，初始化命令行参数列表，解析命令行参数，handle主分发
        :param sys_argv:命令行参数列表
        :return:
        '''
        self.args=sys_argv
        self.argv_parser()  #第一步解析命令行参数
        self.handler()      #第二步连接、认证、指令分发

    def help_conn(self):
        '''
        启动client连接server的帮助信息
        :return:
        '''
        common.show_message(template.MENU_CLIENT_HELP,'INFO')

    def help_instruction(self):
        '''
        登陆成功后的指令帮助菜单
        :return:
        '''
        show_meun=template.INSTRUCTION_MSG.format(self.login_user,self.quotation,self.usedspace)
        common.show_message(show_meun,'INFO')



    def argv_parser(self):
        '''
        解析命令行参数方法
        :return:
        '''
        if len(self.args) < 5:
            common.show_message("命令行参数不符合规范！",'ERROR')
            self.help_conn()
            sys.exit()
        else:
            mandatory_fields=['-p','-s']
            for i in mandatory_fields:
                if i not in self.args:
                    common.show_message("命令行参数不符合规范！",'ERROR')
                    self.help_conn()
                    sys.exit()
            try:
                self.addr=self.args[self.args.index('-s')+1]
                self.port=int(self.args[self.args.index('-p')+1])
            except (IndexError,ValueError):
                common.show_message("命令行参数不符合规范！",'ERROR')
                self.help_conn()
                sys.exit()







    def connect(self,address,port):
        '''
        客户端连接方法
        :return: 登陆codes
        '''
        try:
            self.sock=socket.socket()  #实例化socket
            self.sock.connect((address,port))  #连接socket服务器
            recv_server_data=self.sock.recv(100)  #接受服务端的数据
            if str(recv_server_data,'utf8') == "conn_succ":
                return codes.CONN_SUCC
            else:
                return codes.CONN_FAIL
        except Exception as e:
            client_logger.warn("conn fail:{0}".format(e))
            return codes.CONN_FAIL




    def auth(self):
        '''
        账号密码认证方法
        :return: 认证成功返回True
        '''
        retry_count=0
        while retry_count <3:
            username=common.input_msg("Username:")
            password=common.input_pass("Password:")
            pass_encry=common.encry_sha(password)
            raw_json=json.dumps({
                        'username':username,
                        'password':pass_encry,
                    })
            auth_str="user_auth|%s"%(raw_json)
            self.sock.send(bytes(auth_str,'utf8'))                 #发送用户名和密码过去，发送过去请求认证
            server_response=self.sock.recv(1024)                    #server端发送代码和用户空间信息过来
            server_res_cut=str(server_response,'utf8').split("|")    #将server端发过来的信息cut
            if int(server_res_cut[1]) == codes.AUTH_SUCC:           #认证成功
                self.login_user=username                            #定义一个已经成功登陆成功的用户变量
                self.quotation=server_res_cut[2]                    #用户的磁盘限额
                self.usedspace=server_res_cut[3]                    #用户已经用了的空间
                self.down_path=settings.DOWNLOAD_FILE_PATH          #文件下载路径
                return True
            # elif int(server_res_cut[1]) == codes.AUTH_LOCKED:         #用户被锁
            #     common.show_message("user is alreay locked!!!:{0}".format(username),"ERROR")
            #     client_logger.warn("user is alreay locked!!!:{0}".format(username))
            #     return
            elif int(server_res_cut[1]) == codes.AUTH_USER_ERROR:    #认证失败，用户不存在
                common.show_message("user is not exist:{0}".format(username),"ERROR")
                client_logger.warn("user is not exist:{0}".format(username))
                return
            elif int(server_res_cut[1]) == codes.AUTH_FAIT_PASS:    #用户存在，但是密码错误
                common.show_message("invalid password","ERROR")
                client_logger.error("invalid password")
                retry_count+=1
        else:                                                        #输入错误超过3次
            common.show_message("Too many attempts and user is locked!","ERROR")
            client_logger.error("Too many attempts and user is locked!")




    def interactive(self):
        '''
        账号密码认证成功，交互函数，通过反射进入指令分发方法，put、get、ls、cd、rmf、rmd
        :return:
        '''
        self.logout_flag=False
        while not self.logout_flag:
            if self.login_user:  #如果有这个login_user 变量，代表已经认证成功
                self.help_instruction()
                input_cmd=common.input_msg("[输入命令：]")
                if input_cmd == "quit":
                    self.logout_flag=True
                else:
                    func_cmd=input_cmd.split()[0]
                    try:
                        if hasattr(self,func_cmd):
                            func=getattr(self,func_cmd)
                            func(input_cmd)
                        else:
                            common.show_message("Invalid instruction!","ERROR")
                            client_logger.warn("Invalid instruction for user: {0}".format(self.login_user))
                    except Exception as e:
                        common.show_message(e,"ERROR")
                        client_logger.error(e)

    def get(self,input_cmd):
        '''
        下载文件方法get
        :param input_cmd: get xxx
        :return:
        '''

        if len(input_cmd.split())==1:
            common.show_message("Please Input the remote file which you want to be download!!!","INFO")
            return
        else:
            file_name=input_cmd.split()[1]
            raw_str='get|{0}'.format(file_name)
            self.sock.send(bytes(raw_str,'utf-8'))  #发送get xxx 命令过去客户端

            result=str(self.sock.recv(1024),'utf-8')
            result_cut=result.split("|")
            if result_cut[1] == "file_exists":  #文件存在
                #file_name=input_cmd.split()[1]
                file_abs_path=os.path.join(self.down_path,file_name)
                file_size=int(result_cut[2])
                file_md5=result_cut[3]

                self.sock.send(bytes("{0}".format(codes.TRANS_READY),"utf8"))  #发送ready标示，准备开始接受文件

                recv_size=0
                with open(file_abs_path,'wb') as f:  #开始接收文件
                    while file_size!=recv_size:
                        data=self.sock.recv(4096)
                        recv_size+=len(data)
                        f.write(data)
                        common.print_process(recv_size,file_size)
                    else:
                        client_logger.info("----file:{0} download finished-----".format(file_name))
                        common.show_message("----file:{0} download finished-----".format(file_name),"NOTICE")

                #md5验证
                check_md5=common.encry_md5(file_abs_path)
                if check_md5 == file_md5:
                    client_logger.critical("file:{0} md5 verification  succ!!".format(file_abs_path))
                    common.show_message("file:{0} md5 verification  succ!!".format(file_name),"INFO")
                else:
                    client_logger.info('file:{0} md5 verification not succ!!'.format(file_abs_path))
                    common.show_message('file:{0} md5 verification not succ!!'.format(file_name),"INFO" )

            elif result_cut[1]==codes.IS_DIR:  #是一个目录
                client_logger.warn("{0} is a dir ,not allow download!!!".format(file_name))
                common.show_message("{0} is a dir ,not allow download!!!".format(file_name),"ERROR")
            elif result_cut[1] == codes.FILE_NOT_EXISTS:  #文件不存在
                client_logger.warn("file: {0} is not exists!!!".format(file_name))
                common.show_message("file: {0} is not exists!!!".format(file_name),"ERROR")
            elif result_cut[1] == codes.AUTH_USER_ERROR:  #还没登陆呢
                client_logger.error("you are not login!!!")
                common.show_message("you are not login!!!","ERROR")



    def put(self,input_cmd):
        '''
        上传文件方法,只支持绝对路径
        :param input_cmd: put xxx
        :return:
        '''
        if len(input_cmd.split()) == 1:
            common.show_message("Input the local file which you want to be put!","INFO")
        else:
            abs_file=input_cmd.split()[1] #绝对路径文件
            if os.path.isfile(abs_file):  #首先判断绝对路径文件存不存在
                file_size=int(os.path.getsize(abs_file))  #文件大小
                file_md5=common.encry_md5(abs_file)       #文件md5值

                raw_str="put|{0}|{1}|{2}".format(abs_file,file_size,file_md5)
                self.sock.send(bytes(raw_str,'utf8'))  #发送我要put xxx 消息过去给服务端

                result=str(self.sock.recv(1024),'utf8')  #接受服务端回我的结果： respon|xxx
                result_cut=result.split("|")
                if int(result_cut[1]) == codes.DISK_ENOUGH:  #表示磁盘空间足够，可以开始发送

                    t_start=time.time()
                    put_size=0
                    with open(abs_file,'rb') as f:  #打开文件
                        while file_size!=put_size:
                            data=f.read(4096)
                            self.sock.send(data)
                            put_size+=len(data)
                            common.print_process(put_size,file_size)
                        else:
                            c_time=time.time() - t_start
                            client_logger.info("----file:{0} put finish! and transfer time: {1}---".format(abs_file,c_time))
                            common.show_message("----file:{0} put finish! and transfer time: {1}---".format(abs_file,c_time),"NOTICE")

                            common.show_message("last update usedspace","NOTICE")
                            self.usedspace=str(self.sock.recv(1024),"utf8")  #更新用户最新的已用空间

                elif int(result_cut[1]) == codes.DISK_NOT_ENOUGH:  #空间不足
                    client_logger.error("user:{0} is not enough space to upload file: {1}".format(self.login_user,abs_file))
                    common.show_message("user:{0} is not enough space to upload file: {1}".format(self.login_user,abs_file),"ERROR")
                elif int(result_cut[1]) == codes.AUTH_USER_ERROR:  #还没登陆呢
                    client_logger.error("you are not login!!!")
                    common.show_message("you are not login!!!","ERROR")

            else:
                client_logger.warn("local file:{0} not exist".format(abs_file))   #本地文件不存在
                common.show_message("local file:{0} not exist".format(abs_file),"ERROR")

    def rmf(self,input_cmd):
        '''
        删除文件方法,相对路径
        :param input_cmd: rmf xxx
        :return:
        '''
        if len(input_cmd.split())==1:
            common.show_message("Input the remote file which you want to be delete!","INFO")
            return
        else:
            want_file=input_cmd.split()[1]
            raw_str='rmf|{0}'.format(want_file)
            self.sock.send(bytes(raw_str,"utf8"))  #把'rmf|file' 消息发过去给服务端

            result=str(self.sock.recv(1024),'utf8')  #客户端回的消息“respon|xxx”
            result_cut=result.split("|")
            if int(result_cut[1]) ==codes.DEL_FILE_SUCC:  #删除文件成功
                self.usedspace=result_cut[2]  #更新用户最新的已用空间
                client_logger.info("remove file:{0} succ".format(want_file))
                common.show_message("remove file:{0} succ".format(want_file),"INFO")
            elif int(result_cut[1]) == codes.IS_DIR:      #这是一个目录
                client_logger.warn("want to remove file:{0} but this file is dir !!!".format(want_file))
                common.show_message("want to remove file:{0} but this file is dir !!!".format(want_file),"ERROR")
            elif int(result_cut[1]) == codes.FILE_NOT_EXISTS:  #文件不存在
                client_logger.warn("want to remove file:{0} but this file is not exists!!!".format(want_file))
                common.show_message("want to remove file:{0} but this file is not exists!!!".format(want_file),"ERROR")

    def rmd(self,input_cmd):
        '''
        删除目录方法,相对路径
        :param input_cmd: rmd xxx
        :return:
        '''
        if len(input_cmd.split())==1:
            common.show_message("Input the remote dir which you want to be delete!","INFO")
            return
        else:
            want_dir=input_cmd.split()[1]
            raw_str='rmd|{0}'.format(want_dir)
            self.sock.send(bytes(raw_str,"utf8"))  #把'rmd|dir' 消息发过去给服务端

            result=str(self.sock.recv(1024),'utf8')  #客户端回的消息“respon|xxx”
            result_cut=result.split("|")
            if int(result_cut[1]) ==codes.DEL_DIR_SUCC:  #删除目录成功
                self.usedspace=result_cut[2]  #更新用户最新的已用空间
                client_logger.info("remove dir:{0} succ".format(want_dir))
                common.show_message("remove dir:{0} succ".format(want_dir),"INFO")
            elif int(result_cut[1]) == codes.IS_FILE:      #这是一个文件
                client_logger.warn("want to remove dir:{0} but this dir is file !!!".format(want_dir))
                common.show_message("want to remove dir:{0} but this dir is file !!!".format(want_dir),"ERROR")
            elif int(result_cut[1]) == codes.DIR_NOT_EXISTS:  #目录不存在
                client_logger.warn("want to remove dir:{0} but this dir is not exists!!!".format(want_dir))
                common.show_message("want to remove dir:{0} but this dir is not exists!!!".format(want_dir),"ERROR")

    def cd(self,input_cmd):
        '''
        cd 切换目录
        :param input_cmd: cd xxx
        :return:
        '''
        if len(input_cmd.split()) ==1:
            common.show_message("Input the remote dir which you want to be cd!","INFO")
            return
        else:
            raw_str='cd|{0}'.format(input_cmd.split()[1])
            self.sock.send(bytes(raw_str,'utf8'))  #发送cd xxx 命令过去客户端

            result=str(self.sock.recv((1024)),'utf8')  #获取服务端回我的结果:"xxx|path
            result_cut=result.split("|")
            if result_cut[0]=="alreay_in_homepath":
                common.show_message(result_cut[0],"INFO")
            elif result_cut[0] == "backspace_succ":
                common.show_message(result_cut[0],"NOTICE")
            elif result_cut[0] == "succ_cd_path":
                common.show_message(result_cut[0],"NOTICE")
            elif result_cut[0] == "isn't_dir":
                common.show_message(result_cut [0],"WARN")



    def ls(self,input_cmd):
        '''
        客户端执行ls
        :param input_cmd: 只能是ls
        :return:
        '''
        tmp_flag=False
        while not tmp_flag:
            if len(input_cmd)==2:
                #发送整个ls|过去服务端
                self.sock.send(bytes(input_cmd+"|",'utf8'))
                #接受服务端发送过来的大小信息
                server_ack_msg=self.sock.recv(1024)
                #split这个服务端发过来的信息
                cmd_res_msg=str(server_ack_msg.decode()).split()

                if cmd_res_msg[0] == "CMD_RESULT_SIZE":
                    #获取执行的数据大小
                    cmd_res_size=int(cmd_res_msg[1])

                    #发送回服务端，说我准备接受
                    self.sock.send(b'CLIENT_READY_TO_RECV')

                    #开始接受数据
                    res=''  #定义一个空的结果变量
                    reveived_size=0  #定义一个结果大小变量
                    while reveived_size < cmd_res_size:
                        data=self.sock.recv(1024) #每次接受1024
                        reveived_size+=len(data)
                        res+=str(data.decode())
                    else:
                        common.show_message(res,"INFO")
                        common.show_message("----recv done---","NOTICE")
                        tmp_flag=True
            else:
                common.show_message("invaild command! please agagin!","ERROR")
                tmp_flag=True




    def handler(self):
        '''
        连接，认证，指令分发
        :return:
        '''
        if self.connect(self.addr,self.port) == 200:
            if self.auth():
                self.interactive()
        else:
            common.show_message("ftp-server not start!!!","ERROR")