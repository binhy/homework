#!/usr/bin/env python
#coding=utf-8


import re

#加减
def increase_or_shear(expression):
    while True:
        if ('+-') in expression or ('++') in expression or ('-+') in expression or ('--') in expression:
            expression=expression.replace('+-','-')
            expression=expression.replace('++','+')
            expression=expression.replace('-+','-')
            expression=expression.replace('--','+')
        else:
            break

    expression=expression.lstrip('(').rstrip(')')                                    #把两边()去除掉
    match=re.search("\d+\.*\d*[\+\-]{1}\d+\.*\d*",expression)
    if not match:               #没有匹配到"+","-"的运算
        return expression
    else:
        if len(match.group().split("+")) > 1: #表示加
            num1,num2=match.group().split("+")
            value=float(num1)+float(num2)
        else:                                #表示减
            num1,num2=match.group().split("-")
            value=float(num1)-float(num2)
        tmp=expression.split(match.group())   #把匹配到的分割
        expression="%s%s%s"%(tmp[0],value,tmp[1])   #合并字符串
        increase_or_shear(expression)          #加减递归
    return increase_or_shear(expression)

#乘除
def multiply_divide(expression):
    expression=expression.lstrip('(').rstrip(')')  #把两边()去除掉
    match=re.search("\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*",expression)

    if not match:
        return expression
    else:
        if len(match.group().split("*")) >1: #表示乘
            num1,num2 = match.group().split("*")
            value = float(num1) * float(num2)
        else:                               #表示除
            num1,num2=match.group().split("/")
            value=float(num1) / float(num2)
        tmp=expression.split(match.group())  #把匹配到的分割
        expression="%s%s%s"%(tmp[0],value,tmp[1])  #合并字符串
        multiply_divide(expression)          #乘除递归
    return multiply_divide(expression)

#优先级的执行计算
def compute(expression):
    expression=multiply_divide(expression)   #先乘除
    expression=increase_or_shear(expression)  #后加减
    return expression

#递归括号
def recursion(expression):
    match=re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)',expression) #搜索括号
    if not match:
        print("没有匹配到括号！进入最后一次运算吧！")
        return compute(expression)

    else:
        print("递归括号匹配到:%s"%(match.group()))
        ret=compute(match.group())       #这是计算括号的值
        print("before :%s" %(expression))   #之前的计算表达式
        print("计算匹配到的括号：%s=%s" %(match.group(),ret))
        #print("%s"%(expression.split(match.group())))
        #print("%s"%(expression.split(match.group())[0]))
        #print("%s"%(ret))
        #print("%s"%(expression.split(match.group())[1]))

        expression='%s%s%s' %(expression.split(match.group())[0],ret,expression.split(match.group())[1])  #这里是把匹配到的带括号的表达式进行分割
        print('after :%s'%(expression))
        print("%s上一次计算结束%s"%(8*"=",8*"="))
    return recursion(expression)




#expression="3 - 4 * ( (70-60 +(-2*5-234) * (9-1*5/2 + 9 /2*39/5*2298 +120 * 5368/134 )) + (-2*3)/ (116-33*2) )"
if __name__ =='__main__':
     your_input=input("请输入计算表达式：").strip()
     expression=your_input.replace(' ','')
     print("begin your input: %s" %(expression))
     ret=recursion(expression)
     print("最终的结果:%s"%ret)


