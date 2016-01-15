#!/usr/bin/python
#coding=utf-8
'''
这个是还没上课的时候看pdf写的购物小程序，纯粹练手，比较low，不要看
'''

yu_suan=int(raw_input("please input your budget money: "))
print "welcom you go into my shop!"
print "your budget money:%s" %yu_suan

Item=('1.Air  100','2.coffee  101','3.iphone  102','4.dog  103','5.cat  104','6.exit')
shopping_cart=[]

balance=yu_suan

while True:
    print "这是商品目录:",Item
    your_choice=int(raw_input("please chice your like item:"))
    if your_choice == 1:
        if balance < 100:
            print "您的余额不足，剩余：%d" %balance
            continue
        else:
            balance=balance - 100
    elif your_choice == 2:
        if balance < 101:
            print "您的余额不足，剩余：%d" %balance
            continue
        else:
            balance=balance - 101
    elif your_choice ==3:
        if balance < 102:
            print "您的余额不足，剩余：%d" %balance
            continue
        else:
            balance=balance - 102
    elif your_choice ==4:
        if balance < 103:
            print "您的余额不足，剩余：%d" %balance
            continue
        else:
            balance=balance - 103
    elif your_choice ==5:
        if balance < 104:
            print "您的余额不足，剩余：%d" %balance
            continue
        else:
            balance=balance - 104
    elif your_choice ==6:
        break
    shopping_cart.append(Item[your_choice-1])

print "你购买了:" ,shopping_cart ,"所剩余额：%d" %balance