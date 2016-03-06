#!/usr/bin/env python
#coding=utf-8
__author__ = 'yaobin'

import sys
import re
from core import dump_or_load

#场景类
class all_scene(object):
    def __init__(self,role,we_busman,heroine):
        self.role=role   #初始化一个男角色，hero实例，即是把hero的实例传进来
        self.we_busman=we_busman  #初始化一个武器商人，we_person实例，即是把we_person的实例传进来
        self.heroine=heroine #初始化一个天使引领者，girl实例，即是把gril的实例传进来



    #选择进入哪个场景
    def choice_scene(self):
        '''
        选择进入哪个场景？
        :return:
        '''
        self.break_flag=True
        while self.break_flag:
            self.role_dic=self.role.hero_dic()  #获取hero实例对象的私有普通字段
            main_map='''\033[34;1m
            返回主菜单(r)  存档(s) 查看武器背包（p）
            角色名:%s  角色:%s 等级:%s 手持武器:%s 血量: %s 经验值:%s 钱:%s
            -----------------------------------------------------------

            1.打怪 2.购买武器 3.升级 4.询问天使

            -----------------------------------------------------------
            \033[0m'''%(self.role_dic['name'],self.role_dic['role'],self.role_dic['grade'],self.role_dic['weapon'],self.role_dic['blood_volume'],self.role_dic['exp'],self.role_dic['money'])
            print(main_map)
            ret=input("<<")

            main_menu_dic={"1":self.pk,"2":self.buy,"3":self.update,"4":self.world,"p":self.get_weapon,"r":self.exit}

            if ret in main_menu_dic:
                main_menu_dic[ret]()
            elif ret =="s":
                self.Save_Game(self.role.hero_dic(),self.we_busman.get_we_dic())  #保存角色和商品武器数据
            else:
                print("\033[31;1m输入错误\033[0m")



    #查看武器背包
    def get_weapon(self):
        '''
        查看武器背包方法
        :return:
        '''
        self.role.get_weapon_list()

    #存档
    def Save_Game(self,role_data,we_data):
        '''
        存档方法，要传入两个参数：角色字典和商品武器字典
        :param role_data:
        :param we_data:
        :return:
        '''
        dump_or_load.dump_role_acc(role_data)  #存档人物主角数据
        dump_or_load.dump_we_acc(we_data)      #存档商品武器数据

    #pk
    def pk(self):
        '''
        打怪方法，获取经验值和钱
        :return:
        '''
        msg='''\033[31;1m
        1.暴龙兽 2.加鲁鲁兽 3.飞鹰兽
        \033[0m'''
        print(msg)
        ret=input("请选择你要打的怪：")
        if ret =="1":
            self.role.add_exp(10)
            self.role.add_money(10)
        elif ret=="2":
            self.role.add_exp(15)
            self.role.add_money(15)
        elif ret=="3":
            self.role.add_exp(20)
            self.role.add_money(20)
        else:
            print("\033[31;1m 输入错误，没有这个怪！！\033[0m")


    #购物
    def buy(self):
        '''
        购物方法
        :return:
        '''
        while True:
            tmp=1
            tmp_dic={}  #主要是想生成{顺序号码：武器}
            for i in self.we_busman.get_we_dic(): #获取武器商人武器字典
                print("\033[35;1m %s.武器:%s 数量:%s 金额:%s\033[0m" %(tmp,i,self.we_busman.get_we_dic()[i]['count'],self.we_busman.get_we_dic()[i]['money']))
                tmp_dic[str(tmp)]=i
                tmp+=1
            we_num=input("\033[33;1m 请输入你想买的武器: \033[0m").strip() #输入武器的编号
            if len(we_num)>0 and we_num.isdigit():
                choice_we=tmp_dic[we_num]
                if choice_we in list(tmp_dic.values()):  #判断你选择的武器是否存在
                        choice_num=input("\033[36;1m 请输入购买的数量: \033[0m").strip()
                        if len(choice_num)>0 and choice_num.isdigit(): #判断你输入的数量是否正确
                            pass
                            #if re.match('^\d+$',choice_num):    #判断你输入的数量是否正确
                            if int(choice_num) < self.we_busman.get_we_dic()[choice_we]['count']:  #判断你想买的数量是否大过库存数量:
                                cash=int(self.role.get_money()) #获取现金
                                total=int(choice_num) * self.we_busman.get_we_dic()[choice_we]['money']  #获取总价
                                if total<=cash:  #如果总价<现金，表示你够钱买
                                    self.we_busman.mod_we_dic(choice_we,self.we_busman.get_we_dic()[choice_we]['count']-int(choice_num)) #调用商品武器角色的修改武器方法，修改库存数量
                                    print("%s修改库存数量为:%s"%(choice_we,self.we_busman.get_we_dic()[choice_we]['count']))
                                    self.role.buy_weapons(choice_we,int(choice_num),total)  #调用男主角角色的购买武器方法
                                    continue
                                else:
                                    print("\033[31;1m 现金不够\033[0m")
                            else:
                                print("\033[31;1m 你想要的武器:%s,货存:%s ,不够你想买%s个 \033[0m"%(choice_we,self.we_busman.get_we_dic()[choice_we]['count'],choice_num))
                                continue
                        else:
                            print("\033[31;1m 输入数量错误,请重新输入！\033[0m")
                            continue
                else:
                    print("\033[31;1m 没有这个武器！\033[0m")
                    continue

            elif we_num =="r":
                break
            else:
                print("\033[31;1m不能为空而且必须是选择数字！ \033[0m")





    #升级
    def update(self):
        '''
        升级方法，每次升一级，大于100经验就可以升，比较low，哈哈
        :return:
        '''
        curr_exp=self.role.get_exp()
        judge_up=int(curr_exp-100)
        if  judge_up>=0:
            self.role.update_grade()
            self.role.minus_exp()
        else:
            print("\033[31;1m 还不够经验升级！\033[0m")


    #询问天使
    def world(self):
        '''
        询问天使方法，只要等级大于10和钱大于500 ，就回到现实世界
        :return:
        '''
        self.heroine.say("我是天使引领者，有什么可以帮到你？")
        self.role.say("我想回到现实世界，请验证！")
        if self.role.get_exp() > 10:
            self.heroine.say("恭喜你，你等级通过了！")
            if self.role.get_money()>500:
                self.heroine.say("恭喜你，钱也够了！")
                self.heroine.say("请做好准备，开始传送你回现实世界！")
                self.role.say("哇，好开心，终于要回去了")
                input("喂！！小伙子，你醒醒！！")
                self.role.say("我擦，原来我一直在做梦啊！")
                self.role.say("再也不用打怪了，我会好好珍惜现实生活的！！")
                input("游戏结束，拜拜！~！~！~")
                sys.exit()
            else:
                self.heroine.say("钱不够啊，去赚多点再来找我吧！")
                self.role.say("好吧，继续赚钱去！")
        else:
            self.heroine.say("等级不够，去战斗吧！")
            self.role.say("好吧，继续打怪升级去！！")



    #退出
    def exit(self):
        '''
        退出方法
        :return:
        '''
        self.break_flag=False


