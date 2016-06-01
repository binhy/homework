#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import pika
import subprocess

connection=pika.BlockingConnection(pika.ConnectionParameters(host='42.159.204.94')) #创建连接实例
channel=connection.channel()  #真正控制rabbitmq的实例

channel.exchange_declare(exchange='topic_logs',type='topic') #生成一个订阅，定义exchange，类型是模糊匹配topic
result=channel.queue_declare(exclusive=True)  #不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
queue_name=result.method.queue

channel.queue_bind(exchange='topic_logs',queue=queue_name,routing_key='web.#') #将随机队列和订阅绑定

def CMD(cmd):
    '''
    通过subprocess，执行系统命令
    :param cmd:
    :return: 执行命令的结果，类型是bytes
    '''
    s=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    res=s.stdout.read()
    return res

def on_request(ch,method,props,body):
    '''
    消费者接收到信息后执行的函数
    :param ch:  channel
    :param method:  方法
    :param props:  属性：包含队列名称和id号
    :param body:  接收到的信息
    :return:
    '''

    cmd=body.decode()

    print('Receives the command: {0}'.format(cmd))

    response=CMD(cmd) #执行CMD方法，得到命令结果

    #发回给客户端
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response)
                     )

channel.basic_qos(prefetch_count=1)   #设置prefetchCount=1，则Queue每次给每个消费者发送一条消息；消费者处理完这条消息后Queue会再给该消费者发送一条消息。这是公平分发的方法。
channel.basic_consume(on_request,queue=queue_name,no_ack=True) #定义回调函数on_request  ，指定从queue队列接收消息,no_ack=True表示不用消费者的持久化

print("starting.....")

channel.start_consuming()

