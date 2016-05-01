#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'


import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#print(sys.path)

from modules import main


if __name__ == '__main__':
    main.Main()
