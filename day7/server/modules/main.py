#!/usr/bin/python
#coding=utf-8

import socketserver
from conf import template,settings
from modules import Server,logger,common


ftpserver_logger=logger.logger("start_ftp")



class ArgvHandler(object):
    def __init__(self,args):
        self.args=args
        self.argv_parser()  #指令解析方法


    def help_msg(self):
        print(template.MENU_SERVER)


    def argv_parser(self):
        '''
        解析命令行参数，start或者stop,通过反射，运行start或者stop方法
        :return:
        '''
        if len(self.args)< 2:
            common.show_message("please run start or stop","ERROR")
            self.help_msg()
        else:
            first_argv=self.args[1]
            if hasattr(self,first_argv):
                func=getattr(self,first_argv)
                func()
            else:
                self.help_msg()

    def start(self):
        try:
            server =socketserver.ThreadingTCPServer((settings.FTP_SERVER_IP,settings.FTP_SERVER_PORT),Server.MyTCPHandler)
            server.serve_forever()
        except KeyboardInterrupt:
            common.show_message("----going to shutdown ftp server-----","Error")
            server.shutdown()