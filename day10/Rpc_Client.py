#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import sys
import uuid
import pika
import optparse

def parse_args():
    parser=optparse.OptionParser()

    help='Specify the group name'
    parser.add_option('-g','--Group',action="store",type="string",dest='Group',help=help)
    help='Specify the command executed'
    parser.add_option('-c','--Cmd',action='store',type='string',dest="Cmd",help=help)

    options,args=parser.parse_args()
    if options.Group ==None or options.Cmd == None:
        print(parser.format_help())
        parser.exit()
    else:
        return options




class Rpc_Client(object):
    def __init__(self):
        self.connection=pika.BlockingConnection(pika.ConnectionParameters(host='42.159.204.94')) #创建链接实例
        self.channel=self.connection.channel() #创建控制rabbitmq的实例
        self.channel.exchange_declare(exchange='topic_logs',type='topic') #生成一个可以发接收topic类型的订阅

        result=self.channel.queue_declare(exclusive=True) #不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
        self.callback_queue=result.method.queue

        self.channel.basic_qos(prefetch_count=1) #设置prefetchCount=1，则Queue每次给每个消费者发送一条消息；消费者处理完这条消息后Queue会再给该消费者发送一条消息。这是公平分发的方法。

        self.channel.basic_consume(self.on_response,queue=self.callback_queue) #去 回调队列中消费服务端发过来的数据


    def on_response(self,ch,method,props,body):
        '''
        消费者接收到消息后执行的函数
        :param ch: 相当于channel
        :param method: 具备的方法
        :param props: 属性：包含队列名称和id号
        :param body: 接收到的信息
        :return:
        '''
        if self.corr_id == props.correlation_id:
            self.response=body



    def call(self,group,cmd):
        '''
        向服务端发布命令
        :return: 返回服务端执行结果
        '''

        self.routing_key=group #组名
        self.cmd = cmd  #执行的命令
        self.response=None

        self.corr_id=str(uuid.uuid4())  #将随机值赋给实例的关联id

        self.channel.basic_publish(exchange='topic_logs',
                                   routing_key=self.routing_key,
                                   properties=pika.BasicProperties(  #属性
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,),   #关联id  将随机产生的id赋值给关联id（客户端每次发命令的时候，都带有 不同的随机id，服务端依据指定队列 ,返回执行结果给客户端的时候，客户端依据这个关联id，将执行结果和请求命令对应上
                                   body=self.cmd)
        #如果信息没收到就一直发布
        while self.response is None:
            #开始事件
            self.connection.process_data_events()
        return self.response


options = parse_args()  #生成参数解析之后的结果

rpc=Rpc_Client()
response=rpc.call(options.Group,options.Cmd)

print(response.decode())

