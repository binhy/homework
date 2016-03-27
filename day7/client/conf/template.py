#!/usr/bin/python
#coding=utf-8


MENU_CLIENT_HELP = '''
-s ftp_server_addr    :ftp server ip address, mandatory
-p ftp_server_port    :ftp server port , mandatory
'''

INSTRUCTION_MSG='''
---------------------------------------------------------------
                        FTP CLIENT

User:{0}         quotation:{1} MB         UsedSpace:{2} MB
---------------------------------------------------------------
        get ftp_file        : download file from ftp server
        put local_file      : upload local file to remote
        cd  path            : change dir on ftp server
        rmf file            : del file on ftp server
        rmd dir             : del dir on ftp server
        ls                  : list files on ftp server
        quit                : exit system
'''
