#!/usr/bin/env python
#coding=utf-8

Item={
        1:{"iphone7":7000},
        2:{"ipad_air2":8000},
        3:{"ipad_pro":9000}
    }

#shopping_cart={商品:[金额,数量]}
shopping_cart={}

print(list(Item[1].values())[0])

if list(Item[1].keys())[0] in shopping_cart.keys():
    print('ok')
else:
    print('fail')