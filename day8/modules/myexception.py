#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

class MyException(Exception):

    __errcodes={
        "100":"The login user does not exist！",
        "101":"The list parameter number is not correct!!!",
        "102":"list : The second parameter must -a or -G",
        "103":"d",
        "104":"e",
        "105":"f"

    }


    def __init__(self,errcode):
        self._errcode=errcode


    def __str__(self):
        '''
        如果一个类中定义了__str__方法，那么在打印 对象 时，默认输出该方法的返回值。
        :return:
        '''
        return self.__errcodes[self._errcode]

#
# test=MyExcetion("100")
# print(test)
#
#
#MyExcetion("105")
# print(MyExcetion("105"))