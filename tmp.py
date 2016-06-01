#!/usr/bin/python
#coding=utf-8
__author__ = 'yaobin'

import subprocess

cmd=''
p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.stdout.read()

