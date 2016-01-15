#!/usr/bin/python
#coding=utf-8
'''
还没写完的，不要看
'''

import sys
from collections import Counter

#初始输入金额函数
def budget():
    init_balance=int(raw_input("please input your budget money: "))
    print "your budget money:%s" %init_balance
    return  init_balance

#欢迎函数
def welcome():
    print ('''
    ###############################################
    #           ❤欢迎进入大甩卖商城❤              #
    #             您可以选择以下商品：              #
    #            (1): iphone7    7000             #
    #            (2): ipad_air2  8000             #
    #            (3): ipad_pro   9000             #
    #             w: 结算                         #
    #             z: 对购物车进行整理              #
    #             c: 金额充值                      #
    #             q: 不买了，走人                  #
    ###############################################
    ''')
    init_your_choice=raw_input("please choice your like shop and do somthing:")
    return  init_your_choice


#选择商品函数
def shangpin(num,now_balance):
    if num in Item.keys():
        if now_balance < 7000 or now_balance < 8000 or now_balance < 9000:
            print "您的余额不足，剩余：%d" %now_balance
            return now_balance
        else:
            compute_balance=now_balance - Item[num].values()[0]
            shopping_cart.append(Item[num])
            return compute_balance
    else:
        print("shop is not exist!")
        return now_balance

#结算函数
def balance_accounts(now_balance):
    cost=0
    for i in shopping_cart:
        cost=cost+i.values()[0]
    print("your choice %s,花费 %s,剩余%s")  %(shopping_cart,cost,now_balance)


#金额充值函数
def recharge(now_balance):
    recharge_balance=int(raw_input("please your choice recharge balance"))
    now_balance= now_balance + recharge_balance
    print("充值后你现在总共有%s金额")%now_balance
    return now_balance

#购物车整理函数
def neaten_shopping_cart():
    while True:
        new_shoppinst_cart_list=[]
        for i in shopping_cart:
            new_shoppinst_cart_list.append(i.keys()[0])
        new_shoppinst_cart_dict=Counter(new_shoppinst_cart_list)
        t=1
        for i in new_shoppinst_cart_dict:
            t+=1
            print ("%s:商品：%s,数量：%s") %(t,i,new_shoppinst_cart_dict[i])
            mody_cart=raw_input("请选择商品编号，或者q退出")
            if mody_cart == "q":
                break
                while True:
                    mody_cart_num=raw_input("请输入修改物品的数量:")





#商品字典
Item={
        1:{"iphone7":7000},
        2:{"ipad_air2":8000},
        3:{"ipad_pro":9000}
    }

#购物车
shopping_cart=[]


now_balance=budget()
while True:
    your_choice=welcome()
    if str.isdigit(your_choice):
        now_balance=shangpin(int(your_choice),now_balance)
    elif str.isalpha(your_choice):
        if your_choice == "w":
            balance_accounts(now_balance)
            break
        elif your_choice == "c":
            now_balance=recharge(now_balance)
        elif your_choice == "z":
            neaten_shopping_cart()

        elif your_choice == "q":
             sys.exit()
    #else:


# print "你购买了:" ,shopping_cart ,"所剩余额：%d" %balance