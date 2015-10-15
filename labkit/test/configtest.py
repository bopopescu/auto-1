#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


# 想问个问题, config.py里面用一个函数设置动态地全局变量, 如下

## configtest.py
NUM2=2

def config_varibles():
    NUM=1
    for i in xrange(10):
        globals()['num'+str(i)]=i

if __name__ == '__main__':
    config_varibles()

    print num1,num2,num3  #可以打印出来
#
# 现在想要在另一个文件里面调用config.py里面的函数, 用于设置全局变量, 可是
# # call.py
# from config import *
#
# if __name__ == '__main__':
#     config_varibles()
#     print num1,num2,num3  # 这里会出错, num1, num2, num3名字不存在
#
#
# 目前只想到一个解法就是
# # call.py
# from config import config_varibles
# config_varibles()
# from config import *   #执行完上述函数之后再import一次config中的名字, 这时候就可以了
#
# if __name__ == '__main__':
#     print num1,num2,num3  # 正确打印
#
# 但是觉得两次import 同一个模块好丑陋, 有没有好点的办法