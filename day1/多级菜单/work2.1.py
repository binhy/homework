#!/usr/bin/python
#coding=utf-8
'''
3个while循环，只能输中文选择哦，q退出，b上一级菜单
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


#flag_city=True
while True: #第一个while循环
    for i in info.keys(): #for 循环打印info的3个key出来，即是3个市
        print i,
    input_city=raw_input("please input your city(q/b 退出):") #请求输入市
    if input_city == "b": #如果输入的市是b，则退出
        break
    elif input_city == "q": #如果输入的市是q，则退出
        sys.exit(0)
    elif input_city not in info.keys(): #如果输入的市在info里没有，则重输！
        print "city:%s not exist! please choice again!" %input_city
        continue

#    flag_area=True
    while True:  #第二个while循环，
        print input_city,":",     #打印上一级你选择的city
        for i in info[input_city]: #for循环打印出你选择的市里面的区
            print i,
        input_area=raw_input("please input your area(q/退出,b/上一级):") #请求输入区
        if input_area == "b": #如果输入的区是b，则跳出这层循环，回到上一级循环
            break
        elif input_area == "q": #如果输入的区是q，则退出
            sys.exit(0)
        elif input_area not in info[input_city]: #如果输入的市里面的区在info里没有，则重输
            print "area:%s not exist! please choice again!" %input_area
            continue

#        flag_town=True
        while True: #第三个循环
            print input_area,":", #打印上一级你选择的区
            for i in info[input_city][input_area]: #for循环打印你选择的市里面的区里面的镇！
                print i,
            something=raw_input("please choice (q/退出,b/上一级):") #请求选择退出或者回去上一级菜单
            if something == "b": #如果输入的是b，则跳出这层循环，回到上一级循环
                break
            elif something == "q": #如果输入的是q，则退出
                sys.exit(0)







