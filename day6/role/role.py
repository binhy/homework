#!/usr/bin/env python
#coding=utf-8
__author__ = 'yaobin'

from core import dump_or_load

def already_role():
    '''
    获取已经存在的游戏用户
    :return: 已经存在的游戏用户字典
    '''
    role_name=dump_or_load.load_all_role_name()
    role_dic={}
    for x,i in enumerate(role_name,1):
        role_dic[x]=i

    return role_dic


class ROLE(object):
    '''
    基本人物类
    '''
    def __init__(self,name):
        self.name=name


    def say(self,msg):
        '''
        说话方法
        :param msg: 说的话
        :return: 返回说话是输入内容，用于角色间的交互
        '''
        return input("%s %s"%(self.name,msg))





#男主角
class hero(ROLE):
    '''
    男主角
    '''
    def __init__(self,Role_dic):
        super(hero,self).__init__(Role_dic['name'])
        self.__role=Role_dic['role']
        self.__weapon=Role_dic['weapon']
        self.__weapon_list=Role_dic['weapon_list']
        self.__grade=Role_dic['grade']
        self.__blood_volume=Role_dic['blood_volume']
        self.__money=Role_dic['money']
        self.__exp=Role_dic['exp']


    def hero_dic(self):
        '''
        因为都是私有普通字段，所有要整个这个方法，从类内部访问
        :return: 男主角数据字典
        '''
        hero_dic={
            'name':self.name,
            'role':self.__role,
            'weapon':self.__weapon,
            'weapon_list':self.__weapon_list,
            'grade':self.__grade,
            'blood_volume':self.__blood_volume,
            'money':self.__money,
            'exp':self.__exp
        }
        return hero_dic


    def get_weapon_list(self):
        '''
        获取背包
        :return:
        '''
        myset=set(self.__weapon_list)
        for i in myset:
            print("\033[32;1m武器: %s 数量: %s\033[0m"%(i,self.__weapon_list.count(i)))


    def add_exp(self,num):
        '''
        增加经验值方法
        :param num:
        :return: 增加经验后的经验
        '''
        self.__exp+=num
        print("\033[32;1m 角色:%s 增加经验:%s\033[0m"%(self.name,num))
        return self.__exp

    def add_money(self,num):
        '''
        增加钱方法
        :param num:
        :return: 增加钱后的钱
        '''
        self.__money+=num
        print("\033[32;1m角色:%s 增加钱:%s\033[0m"%(self.name,num))
        return self.__money

    def get_money(self):
        '''
        获取我有多少钱
        :return: 钱
        '''
        return self.__money

    def buy_weapons(self,weapon_name,count,price):
        '''
        购买武器方法
        :param weapon_name: 武器名字
        :param count:  购买的数量
        :param price:  武器的价格
        :return:
        '''
        for i in range(count):
            self.__weapon_list.append(weapon_name)

        self.__money-=price

    def get_exp(self):
        '''
        获取我现在有多少经验
        :return: 经验
        '''

        return self.__exp

    def update_grade(self):
        '''
        升级，比较low，每次只升一级
        :return: 等级
        '''
        self.__grade=self.__grade+1
        print("\033[32;1m 恭喜你升级！当前等级为:%s\033[0m"%(self.__grade))
        return self.__grade

    def minus_exp(self):
        '''
        每次升级完，减去当前经验100
        :return: 经验
        '''
        self.__exp=self.__exp-100
        return self.__exp

#武器商人
class we_person(ROLE):
    '''
    武器商人
    '''
    def __init__(self,name):
        super(we_person,self).__init__(name)
        self.__we_dic=dump_or_load.load_weapon_dic()


    def get_we_dic(self):
        '''
        获取商品武器字典
        :return: 商品武器字典
        '''

        return self.__we_dic


    def mod_we_dic(self,weapon,count):
        '''
        修改武器库存
        :param weapon:
        :param count:
        :return: 返回一个武器库字典
        '''
        self.__we_dic[weapon]['count']=count
        return self.__we_dic





#天使引领者
class girl(ROLE):
    '''
    女主角
    '''
    def __init__(self,name):
        super(girl,self).__init__(name)



