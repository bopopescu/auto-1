#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:

    tmpelate.py  [-q | --quiet] [-l | --log] [-d | --debug]
    tmpelate.py (-h | --help)
    tmpelate.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my tmpelate
"""




#
#
# if __name__ == '__main__':
#     main()



class A:
    a=0
    b=0
    def hello(self):
        print self.a,self.b
self
a=A()
a.c=1
print a.c
a.__class__.c=4
print A.c

def run(s):
    s='haha'
s=A()
s.s='good'
run(s)
print s