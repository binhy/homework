Modify_haproxy.py README
===============

##详解
view() #查看函数
add_backend() #增加函数
del_backend() #删除函数

##example view
[root@localhost python]# python modify_haproxy.cfg

        ###############################################
        #           ❤欢迎进入修改haproxy.cfg❤        #
        #            您有以下选择：                    #
        #            (1): 查看backend记录             #
        #            (2): 增加backend记录             #
        #            (3): 删除backend记录             #
        #            (q): 退出                        #
        ###############################################

please choice your like record and do somthing:1
please choice your like backend:web
[[web backend的server记录是：]]
server 192.168.10.20 weight 20 maxconn 5000
server 192.168.10.21 weight 40 maxconn 3000
server 192.168.10.111 weight 30 maxconn 1000
...
omit...
...
please choice your like record and do somthing:q
good bye!!!!


##example add
[root@localhost python]# python modify_haproxy.cfg

        ###############################################
        #           ❤欢迎进入修改haproxy.cfg❤        #
        #            您有以下选择：                    #
        #            (1): 查看backend记录             #
        #            (2): 增加backend记录             #
        #            (3): 删除backend记录             #
        #            (q): 退出                        #
        ###############################################

please choice your like record and do somthing:2
请输入要新增加的记录:{"backend": "db","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
...
omit...
...
please choice your like record and do somthing:q
good bye!!!!


##example del
[root@localhost python]# python modify_haproxy.cfg

        ###############################################
        #           ❤欢迎进入修改haproxy.cfg❤        #
        #            您有以下选择：                    #
        #            (1): 查看backend记录             #
        #            (2): 增加backend记录             #
        #            (3): 删除backend记录             #
        #            (q): 退出                        #
        ###############################################

please choice your like record and do somthing:3
请输入要删除的记录:{"backend": "db","record":{"server": "192.168.10.30","weight": 40,"maxconn": 5000}}
...
omit...
...
please choice your like record and do somthing:q
good bye!!!!