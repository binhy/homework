# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import socket
import sys
from paramiko.py3compat import u
import models ,datetime

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan,user_obj,bind_host_obj,cmd_caches,log_recording):
    if has_termios:
        posix_shell(chan,user_obj,bind_host_obj,cmd_caches,log_recording)
    else:
        windows_shell(chan)


def posix_shell(chan,user_obj,bind_host_obj,cmd_caches,log_recording):
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        cmd = ''

        tab_key = False
        while True:
            # 监视 用户输入 和 远程服务器返回数据（socket）
            # 阻塞，直到句柄可读
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:  #如果远程服务器有数据库返回
                try:
                    x = u(chan.recv(1024))
                    if tab_key:  #如果tab键为True
                        if x not in ('\x07' , '\r\n'): #如果没有这些字符
                            #print('tab:',x)
                            cmd += x              #你输入的命令+=cmd
                        tab_key = False
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:  #你自己有输入东西
                x = sys.stdin.read(1)  #每次读1个字符？
                if '\r' != x:  #如果输入不是回车，+=cmd
                    cmd +=x
                else:
                    print('cmd->:',cmd)
                    log_item = models.AuditLog(user_id=user_obj.id,
                                          bind_host_id=bind_host_obj.id,
                                          action_type='cmd',
                                          cmd=cmd ,
                                          date=datetime.datetime.now()
                                          )
                    cmd_caches.append(log_item)
                    cmd = ''

                    if len(cmd_caches)>=10:  #alex 这里使用了缓存
                        log_recording(user_obj,bind_host_obj,cmd_caches)
                        cmd_caches = []
                if '\t' == x:  #如果输入有tab键
                    tab_key = True
                if len(x) == 0:
                    break
                chan.send(x)  #发送过去远程服务器

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass