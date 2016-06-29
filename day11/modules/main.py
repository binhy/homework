#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'


from conf import template
from modules import common,session
from dbhelper import db_api

def main():
    print(template._1_MENU)
    choice=common.input_msg(">:")
    if choice == "1":
        session.start_session()
    elif choice == "2":
        inst=db_api.init_db()
    else:
        common.color_print("not this choice!",exits=True)

