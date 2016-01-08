#!/usr/bin/python
#coding=utf-8
'''
3个while循环，每次执行要么全部输入中文，要么全部输入数字。
不能第一次输数字，第二次输字符,也不能第一次输中文，第二次输数字
q退出，b上一级菜单
'''

import sys
info={

        "广州市":{
        "番禺区":["石楼镇","石碁镇","洛溪镇","大岭镇","官桥镇"],
        "海珠区":["耳朵镇","日诶镇","娃儿镇","技能镇","哦哦镇"],
        "天河区":["回复镇","很多镇","黄飞镇","洛可镇","而我镇"],
        },



    "深圳市":{
        "福田区":["儿童镇","请问镇","有地镇","藕片镇","谈定镇"],
        "罗湖区":["地方镇","人头镇","内存镇","额外镇","哦的镇"],
        "宝安区":["地间镇","日他镇","俄儿镇","我能镇","摊位镇"],
        },



    "佛山市":{
        "禅城区":["还有镇","李丹镇","欧派镇","趣味镇","单反镇"],
        "南海区":["而我镇","欧鹏镇","吃到镇","快捷镇","恶疾镇"],
        "高明区":["大基镇","看到镇","大口镇","你看镇","短发镇"],
        }

}

while True: #第一个while循环
    city_list=info.keys() #获取全部城市，生成一个城市列表
    city_dict={} #定义一个城市字典
    for index,value in enumerate(city_list,1): #枚举城市列表
        city_dict[index]=value #index:位置(1.2.3.4) ,value:城市
        print index,value, #打印位置，城市
    input_city=raw_input("please input your city(q/b 退出):") #请求输入市
    if str.isdigit(input_city):  #对输入是否数字进行判断
        input_city=int(input_city) #如果是数字，转换为整形
    else:
        input_city=str(input_city) #不是，那么转化为字符
    if input_city == "b": #如果输入的市是b，则退出
        break
    elif input_city == "q": #如果输入的市是q，则退出
        sys.exit(0)
    elif input_city in city_dict.keys(): #如果你输入的是城市数字，那么判断是否在city_dict的key
        final_city=input_city
    elif input_city in city_dict.values(): #如果你输入的是城市字符，那么判断是否在city_dict的value
        final_city=input_city
    else:
        print "city:%s not exist! please choice again!" %input_city #前面都不是，那么没有这个城市罗，请重输
        continue


    while True:  #第二个while循环，
        if type(final_city) == str:    #如果你最终选择的城市是字符
            print final_city,":",     #打印上一级你选择的城市字符
            area_list=info[final_city].keys()  #获取你选择的这个城市的全部区，生成这个城市的区列表
            area_dict={} #定义一个区字典
            for index,value in enumerate(area_list,1): #枚举区列表
                area_dict[index]=value  #index:位置(1.2.3.4) ,value:区
                print index,value, #打印位置和区
        elif type(final_city) == int:  #如果你最终选择的城市是数字
            final_city2=city_dict[final_city]  #重新定义一个最终城市变量，目的是获取这个城市数字对应的城市字符
            print final_city2,":",     #打印上一级你选择的城市
            area_list=info[final_city2].keys()  #获取你选择的这个城市的全部区，生成这个城市的区列表
            area_dict={} #定义一个区字典
            for index,value in enumerate(area_list,1): #枚举区列表
                area_dict[index]=value #index:位置(1.2.3.4) ,value:区
                print index,value, #打印位置和区
        input_area=raw_input("please input your area(q/退出,b/上一级):") #请求输入区
        if str.isdigit(input_area): #对输入是否数字进行判断
            input_area=int(input_area) #如果是数字，转换为整形
        else:
            input_area=str(input_area)  #不是，那么转化为字符
        if input_area == "b": #如果输入的区是b，则跳出这层循环，回到上一级循环
            break
        elif input_area == "q": #如果输入的区是q，则退出
            sys.exit(0)
        elif input_area in area_dict.keys(): #如果你输入的是区数字，那么判断是否在area_dict的key
            final_area=input_area
        elif input_area in area_dict.values(): #如果你输入的是区字符，那么判断是否在area_dict的value
            final_area=input_area
        else:
            print "area:%s not exist! please choice again!" %input_area #前面都不是，那么没有这个区罗，请重输
            continue



        while True: #第三个循环
            if type(final_area) ==str:  #如果最终你选择的是区字符
                print final_area,":", #打印上一级你选择的区字符
                town_list=info[final_city][final_area] #获取你选择的这个区的全部镇，生成这个区的镇列表
                for index,value in enumerate(town_list,1): #枚举镇列表，目的是打印位置和镇
                    print index,value, #打印位置和镇
            elif type(final_area) == int: #如果最终你选择的是区数字
                final_area2=area_dict[final_area] ##重新定义一个最终区变量，目的是获取这个区数字对应的区字符
                print final_area2,":", #打印上一级你选择的区字符
                town_list=info[final_city2][final_area2] #获取你选择的这个城市的区的全部镇，生成这个城市的区的全部镇列表
                for index,value in enumerate(town_list,1): #枚举镇列表
                     print index,value, #打印位置和镇
            something=raw_input("please choice (q/退出,b/上一级):") #请求选择退出或者回去上一级菜单
            if something == "b": #如果输入的是b，则跳出这层循环，回到上一级循环
                break
            elif something == "q": #如果输入的是q，则退出
                sys.exit(0)









