#################################################
# Created on: 2016年06月01日
# @author: 陈耀斌
# Email: 123391713@qq.com
# Blog: http://www.cnblogs.com/binhy0428/
# GitHub: https://github.com/binhy/
#################################################


一.功能说明：
本程序是一个rabbit_mq rpc机制，exchange=topic，批量执行命令的sb程序,要自己修改server端的routing_key,才能自定义组。



二.运行说明:
server: e.g: python3 Rpc_Server.py
client: e.g: python3 Rpc_Client.py -g web -c ifconfig


三.用到主要知识点
1.模块：pika
2.知识点： 函数、类



