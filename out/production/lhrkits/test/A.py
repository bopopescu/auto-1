#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


class A():

    def method_a(self):
        pass

class B():
    def method_b(self):
        self.a=A()
        return self.a



if __name__ == '__main__':
    b=B()
    a=A()
    aa=b.method_b()
    aa.method_a()


