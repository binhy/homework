#!/usr/bin/env python
#coding=utf-8
__author__ = 'yaobin'

import re


#expression="3 - 4 * ( (70-60 +(-42*5-100*215) * (9-1*5/2 + 9 /2*39/5*2298 +120 * 5368/134 )) - (-42*3)/ (116-33*2) )"
expression="1 - 2 *  (60-30 +(-40/5))"
#content=re.search("\(([\+\-\*\/.]?\d+){2,}\)",expression)
content=re.search("\(([\+\-\*\/]*\d+\.*\d*){2,}\)",expression)
# print(content.group())
print(content.group())
a=expression.split(content.group())
print(a[0])
print(a[1])

expression="2*22.0"
num1,num2=expression.split("*")
# print("%s"%(expression.split("*")))
# print(len(expression.split("*")))
print(num1,num2)
# content2=re.search("[\-\+]?\d+[\*\/]?\d+",content.group())
# if content2:
#     print("yes %s"%(content2.group()))
# else:
#     print("no!!")
#content2=re.search("[\d+\.*\d*[\+\-]{1}\d+\.*\d*]",content.group())
#print(content2)

# print(content.group(1))
# #print(type(content.group()))
# print(len(content.group()))

# content2=content.group().lstrip("(").rstrip(")")
# print(content2.split('*'))
#print(content.group().split('-'))
#content=content[1:len(content)-1]
#print(content)