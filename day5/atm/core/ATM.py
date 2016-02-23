# #!/usr/bin/env python
# #coding=utf-8
#
# import os,sys
# import random
# base_dir=os.path.dirname(os.path.dirname(__file__))
# sys.path.append(base_dir)
# #print(sys.path)
#
# from logger.record_log import  Logger
#
# #选择函数
# def ATM_operation():
#     choice=input("请选择1:办卡 2:登陆")
#     if choice=="1":
#         add_card()
#     elif choice=="2":
#         login(6)
#     else:
#         print("error!")
#
#     return
#
#
# #办卡函数
# def add_card():
#
#
#
# #验证码函数
# def verification_code(func):
#     def inner(length):
#         check_code = ""
#         for i in range(length):
#             current = random.randint(0,4)
#             if current != i :
#                 tmp = str(chr(random.randint(65,90)))
#             else:
#                 tmp = random.randint(0,9)
#             check_code += str(tmp)
#         print("验证码:%s"%check_code)
#         your_input=input("请输入验证码:")
#         if your_input == check_code:
#             return func(length)
#         else:
#             print("验证码输入错误！！")
#             return None
#     return inner
#
#
#
#
# #登陆函数
# @verification_code
# def login(length):
#     user=input("请输入帐号:")
#     password=input("请输入密码:")
#
#
#
#
#
#
#
#
#
# #