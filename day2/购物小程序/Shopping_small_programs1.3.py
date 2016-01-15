#!/usr/bin/python
#coding=utf-8
'''
最终版商城购物
'''
import sys

#选择登陆，还是注册
def begin():
    global flag
    while True:
        print("欢迎进入大甩卖商城，您目前可以有两个选择，1.登陆，2.注册\n")
        init_choice=raw_input("请选择：")
        if init_choice == "1":
            flag=login() #获取login()函数返回的True or False
            break
        elif init_choice =="2":
            register()  #调用注册函数
            continue
        else:
            print("输入错误，只可以输入1或者2，请重新输入！\n")
            continue
    return flag #返回login()函数返回的True or False

#注册函数
def register():
    while True:
        register_user=raw_input("请输入注册用户名：\n")
        already_register_user=[]  #已经注册用户列表
        check_user_file=open("account.txt","r")
        for i in check_user_file.readlines():
            already_register_user.append(i.split()[0]) #把获取的已经注册了的用户追加到已经注册用户列表
        check_user_file.close()

        if register_user in already_register_user: #判断输入的用户名是否在已经注册用户列表
            print("用户已经存在，请换一个！")
            continue
        else:
            register_passwd=raw_input("请输入注册密码：\n")
            print("恭喜您注册成功！")
            account_file=open("account.txt","a") #把新注册的用户名和密码追加到帐号密码文件
            print >> account_file,register_user,register_passwd
            account_file.close()
            break

#登陆函数
def login():
    flag=True
    username=raw_input("请输入登陆用户名:")
    account_dict={} #定义一个空的帐号密码字典
    lock_user_list=[] #定义一个空的锁用户列表

##初始化帐号密码文件，生成一个帐号密码字典
    with open('account.txt') as f:
        account_passwd=f.readlines()
        for i in account_passwd:
            account_dict[i.split()[0]]=i.split()[1]
    #print account_dict

##初始化锁定用户文件，生成一个已被锁用户列表
    with open('lock_user.txt') as f:
        for i in f:
            lock_user_list.append(i.strip())
    #print lock_user_list

##开始循环
    count=0
    while count < 3:
        if username in lock_user_list:    #判断用户是否被锁
            print "帐号:%s 被锁！" %username
            flag=False #标记改为False
            break
        else:
            if username in account_dict:  #判断是否有这个用户
                passwd=raw_input("请输入密码:")  #有这个用户，那么请输入密码
                if passwd == account_dict[username]:  #判断密码是否正确
                    print "恭喜你:%s 用户登陆成功！\n" %username
                    break
                else:
                    count +=1              #密码不正确，可以重输3次
                    continue
            else:
                 print "用户:%s 不存在!" %(username) #打印帐号不存在
                 flag=False  #标记改为False
                 break   #没有这个用户，就break，退出循环

    else:
        print("您已经输错密码超过3次,抱歉:%s 用户被锁了 !") %(username) #打印输错3次密码，并且锁定该用户
        flag=False
        lock_file=open("lock_user.txt","a")
        print >> lock_file,username #追加用户到锁文件
        lock_file.close() #关闭锁文件
    return flag #函数返回flag标记，True or False

#预算金额函数
def budget():
    global init_balance
    while True:
        init_balance=raw_input("购物之前，请输入您的预算金额: ")
        if len(init_balance)==0:
            print("输入不能为空！请重新输入！\n")
            continue
        elif str.isalpha(init_balance):
            print("输入预算金额错误，请重新输入！\n")
            continue
        else:
            print "您的预算金额为:%s" %init_balance
            break
    return  int(init_balance)


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
    return  init_your_choice   #你选的是啥？


#选择商品函数
def shangpin(num,surplus_balance):
    if num in Item.keys():   #你选择的存在商品字典里
        if surplus_balance < 7000 or surplus_balance < 8000 or surplus_balance < 9000:
            print "您的余额不足，剩余：%d" %surplus_balance
            return surplus_balance
        else:
            compute_balance=surplus_balance - Item[num].values()[0]  #计算余额
            if shopping_cart_dict.has_key(Item[num].keys()[0]):  #如果商品已经买过
                shopping_cart_dict[Item[num].keys()[0]][1]=shopping_cart_dict[Item[num].keys()[0]][1] + 1  #那么在购物车里的这个商品数量+1
                return compute_balance  #返回一个计算过的余额
            else:                           #如果商品没有买过,初始化购物车这个商品数量为1
                init_num=1
                shopping_cart_dict[Item[num].keys()[0]]=[Item[num].values()[0],init_num]
                return compute_balance #返回一个计算过的余额
    else:  #你选择的不存在商品字典
        print("shop is not exist!")
        return surplus_balance #返回最初的金额

#结算函数
def balance_accounts(surplus_balance):
    all_cost=0  #初始化一个总花费变量等于0
    for i in shopping_cart_dict: #遍历循环购物车字典
        all_cost=all_cost + shopping_cart_dict[i][0] * shopping_cart_dict[i][1] #shopping_cart_dict[i][0] * shopping_cart_dict[i][1] 的意思是：金额x数量
        print("您最终的选择： 商品:%s，数量:%s,商品花费: %s")  %(i,shopping_cart_dict[i][1],shopping_cart_dict[i][0] * shopping_cart_dict[i][1])
    print ("总花费：%s,剩余金额：%s") %(all_cost,surplus_balance)


#金额充值函数
def recharge(surplus_balance):
    global now_balance
    while True:
        recharge_balance=raw_input("please your choice recharge balance:")
        if len(recharge_balance) ==0:
            print("输入不能为空，请重新输入！")
            continue
        elif str.isalpha(recharge_balance):
            print("输入金额错误，请重新输入！")
            continue
        else:
            now_balance= surplus_balance + int(recharge_balance)
            print("充值后你现在总共有%s金额\n")%now_balance
            break
    return now_balance

#购物车整理函数
def neaten_shopping_cart(surplus_blance):
    global surplus_balance #全局变量，为啥呢？还没弄懂？继续学习，回头再理解吧
    while True: #第一层循环
        for i in shopping_cart_dict: #循环商品字典
            print("您目前的选择： 商品:%s，数量:%s,商品花费: %s")  %(i,shopping_cart_dict[i][1],shopping_cart_dict[i][0] * shopping_cart_dict[i][1])

        product_id=raw_input("请选择商品编号（1:iphone7, 2:ipad_air2, 3:ipad_pro），或者q退出:\n")
        if product_id == "q":  #输入q，退出第一层循环
            break
        if len(product_id) ==0:
            print("输入不能为空，请重新输入！\n")
            continue
        if str.isalpha(product_id) or int(product_id) not in Item.keys() or Item[int(product_id)].keys()[0] not in shopping_cart_dict.keys():  #编号是字符 or 编号不存在商品字典 or 编号不存在购物车里
            print ("输入错误，购物车字典没有这个商品或者商品字典没有这个商品编号，请重新输入！\n")
            continue   #重新输入吧！
        elif str.isalnum(product_id): #编号是数字
            while True:  #第二层循环
                mody_shop_num=raw_input("请输入修改%s的数量:(注意0是代表删除哦):\n" %(Item[int(product_id)].keys()[0]))
                if len(mody_shop_num)==0:
                    print("输入不能为空，请重新输入！\n")
                    continue
                if str.isalpha(mody_shop_num):   #判断输入修改数量的是否字符，是字符就continue，重新输入吧！
                    print("输入错误！请输入数字！\n")
                    continue
                elif mody_shop_num == "0":      #判断修改数量是否为0，是0代表删除这个商品！
                    surplus_balance=surplus_balance + shopping_cart_dict[Item[int(product_id)].keys()[0]][0] * shopping_cart_dict[Item[int(product_id)].keys()[0]][1] #重新计算余额，删除的这个商品的金额，要退回去我的余额里呢
                    del shopping_cart_dict[Item[int(product_id)].keys()[0]]  #删除购物车字典里的商品！
                    break  #退出第二层循环

                elif mody_shop_num != "0":      #如果输入的不是字符也不是数字0，那就是修改商品的数量>0了！
                    if int(mody_shop_num) == shopping_cart_dict[Item[int(product_id)].keys()[0]][1]:  #修改商品的数量=购物车的数量
                        print ("修改商品的数量等于购物车的数量啦！！没什么用啊！你妹的，修改别的啊！\n")
                        break  #退出第二层循环
                    elif int(mody_shop_num) < shopping_cart_dict[Item[int(product_id)].keys()[0]][1]:  #修改商品数量<购物车数量
                        retrogress_num=shopping_cart_dict[Item[int(product_id)].keys()[0]][1] - int(mody_shop_num)  #删除这个商品的数量
                        surplus_balance = surplus_balance + shopping_cart_dict[Item[int(product_id)].keys()[0]][0] * retrogress_num #删除这个商品数量的金额要回退到我的余额里呢
                        shopping_cart_dict[Item[int(product_id)].keys()[0]][1] = int(mody_shop_num)  #修改这个商品在购物字典里的数量
                        break  #退出第二层循环

                    elif int(mody_shop_num) > shopping_cart_dict[Item[int(product_id)].keys()[0]][1]: #修改商品数量>购物车数量
                        increase_num=int(mody_shop_num) - shopping_cart_dict[Item[int(product_id)].keys()[0]][1] #计算增加了多少个商品
                        increase_shop_balance = shopping_cart_dict[Item[int(product_id)].keys()[0]][0] * increase_num #计算增加这几个商品的金额
                        if surplus_balance < increase_shop_balance: #增加这几个商品的金额<余额
                             print ("金额不足！你想增加:%s商品数量为:%s,增加金额:%s,增加金额大于你的所剩金额%s!!!\n") %(Item[int(product_id)].keys()[0],increase_num,increase_shop_balance,surplus_balance)
                             break   #退出第二层循环
                        else:  #不是，那么就是够余额买增加的商品数
                            shopping_cart_dict[Item[int(product_id)].keys()[0]][1] = int(mody_shop_num) #修改这个商品在购物字典里的数量
                            surplus_balance=surplus_balance-increase_shop_balance #重新计算余额，余额 - 增加的商品的金额
                            break #退出第二层循环
                    else:
                        pass
                else:
                    print("修改物品数量错误！请重新输入！")
                    continue
        else:
            print("输入错误！")
            continue
    return surplus_balance #返回余额

#商品字典
Item={
        1:{"iphone7":7000},
        2:{"ipad_air2":8000},
        3:{"ipad_pro":9000}
    }

#购物车字典
#shopping_cart={商品:[金额,数量]}
shopping_cart_dict={}


#主循环
if __name__ == "__main__":
    if begin(): #其实这里是获取login()函数的True or False，其实只有两种情况会False，①帐号被锁、②用户不存在。如果出现这两种情况，那么不进入下面的循环啦。
        surplus_balance=budget()  #第一次执行，调用budget函数，初始化预算=余额
        while True:
            your_choice=welcome()  #调用欢迎函数，你输入的是？
            if str.isdigit(your_choice):  #输入的选择是数字，调用商品函数
                surplus_balance=shangpin(int(your_choice),surplus_balance)
            elif str.isalpha(your_choice): #输入的是字符
                if your_choice == "w":
                    balance_accounts(surplus_balance)  #调用结算函数
                    break
                elif your_choice == "c":
                    surplus_balance=recharge(surplus_balance) #调用金额充值函数
                elif your_choice == "z":
                    surplus_balance=neaten_shopping_cart(surplus_balance) #调用整理购物车函数
                elif your_choice == "q":
                     sys.exit()
            else:
                print("输入错误，请重输！")
    else:
         pass
