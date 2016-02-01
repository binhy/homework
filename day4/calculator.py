#!/usr/bin/env python
#coding=utf-8


import re

#加减
def increase_or_shear(expression):
    #print("加减%s"%expression)
    while True:
        if ('+-') in expression or ('++') in expression or ('-+') in expression or ('--') in expression:
            expression=expression.replace('+-','-')
            expression=expression.replace('++','+')
            expression=expression.replace('-+','-')
            expression=expression.replace('--','+')
        else:
            break


    #expression=expression.lstrip("(").rstrip(")")
    #match=re.search("[\-\+]?\d+[\*\/]?\d+",expression)
    expression=expression.lstrip('(').rstrip(')')
    match=re.search("\d+\.*\d*[\+\-]{1}\d+\.*\d*",expression)
    if not match:
        return expression
    else:
        if len(match.group().split("+")) > 1: #表示加
            num1,num2=match.group().split("+")
            value=float(num1)+float(num2)
        else:                                #表示减
            num1,num2=match.group().split("-")
            value=float(num1)-float(num2)
        tmp=expression.split(match.group())
        expression="%s%s%s"%(tmp[0],value,tmp[1])
        increase_or_shear(expression)
    return increase_or_shear(expression)

#乘除
def multiply_divide(expression):
    #match=re.search("\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*]",expression)
    expression=expression.lstrip('(').rstrip(')')
    #match=re.search("[\-\+]?\d+[\*\/]?\d+",expression)
    match=re.search("\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*",expression)

    if not match:
        return expression
    else:
        #print(match.group())
        if len(match.group().split("*")) >1: #表示乘
            num1,num2 = match.group().split("*")
            value = float(num1) * float(num2)
        else:                               #表示除
            num1,num2=match.group().split("/")
            value=float(num1) / float(num2)
        tmp=expression.split(match.group())
        expression="%s%s%s"%(tmp[0],value,tmp[1])
        multiply_divide(expression)
    return multiply_divide(expression)

#优先级的执行计算
def compute(expression):
    expression1=multiply_divide(expression)
    #print("%s"%(expression1))
    expression2=increase_or_shear(expression1)
    print("%s"%(expression2))
    return expression2

#递归括号
def recursion(expression):
    match=re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)',expression)
    if not match:
        print("没有匹配到括号！进入最后一次运算吧！")
        return compute(expression)
        #ret=compute(expression)
        #print("%s"%(ret))
    else:
        print("递归括号匹配到:%s"%(match.group()))
        ret=compute(match.group())
        print("before :%s" %(expression))
        print("计算匹配到的括号：%s=%s" %(match.group(),ret))
        #print("%s"%(expression.split(match.group())))
        #print("%s"%(expression.split(match.group())[0]))
        #print("%s"%(ret))
        #print("%s"%(expression.split(match.group())[1]))

        expression='%s%s%s' %(expression.split(match.group())[0],ret,expression.split(match.group())[1])
        print('after :%s'%(expression))
        print("%s上一次计算结束%s"%(8*"=",8*"="))
    return recursion(expression)




#expression="3 - 4 * ( (70-60 +(-42*5-234) * (9-1*5/2 + 9 /2*39/5*2298 +120 * 5368/134 )) - (-42*3)/ (116-33*2) )"
if __name__ =='__main__':
     your_input=input("请输入计算表达式：").strip()
     expression=your_input.replace(' ','')
     print("begin your input: %s" %(expression))
     recursion(expression)
