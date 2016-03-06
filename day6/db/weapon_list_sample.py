#!_*_coding:utf-8_*_
#__author__:"Alex Li"


#weapon_list=["双节棍":,"巨型飞镖","青龙偃月刀"]
import json
weapon_list = {
     '双节棍':{'money':10,'count':10},
     '巨型飞镖':{'money':20,'count':20},
     '青龙偃月刀':{'money':30,'count':30},
}
print(json.dumps(weapon_list))