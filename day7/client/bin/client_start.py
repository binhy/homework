#!/usr/bin/python
#coding=utf-8

import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules import client

if __name__ == '__main__':
    client.Client(sys.argv)
