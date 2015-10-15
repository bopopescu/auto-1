#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


def as_method_of(cls):
    "修饰方法使其成为类的方法, 方法需要带有self参数, 会成为类的unbounded和对象的bounded方法"
    def as_method_of_cls(func):
        setattr(cls,func.__name__,func)
    return as_method_of_cls


from A import *

# class A(A):
#     def new_method(self):
#         print "added new"
#

@as_method_of(A)
def new_method(self):
    print "added new"


@as_method_of(A)
def method_a(self):
    print "this is new method_a"


# todo: 为什么这样不行


# as_method_of_cls(A.A,new_method)

if __name__ == '__main__':
    a=A()
    b=B().method_b()
    # A.A.new_method=staticmethod(new_method)

    b.new_method()
    b.method_a()
    print b.new_method
    print a.method_a
    print A.method_a

exit(0)


class AddHigh(object):
    """ 给长方形添加高变成长方体 """
    def __init__(self, cls, z):
        self._cls = cls
        self._z = z

    def __call__(self, *args, **kwargs):
        # 重写面积计算方式
        def _area(this, *args, **kwargs):
            return (self._z * this._x + self._z * this._y + this._x * this._y) * 2

        self._cls.area = _area
        obj = self._cls(*args, **kwargs)
        return obj


class Rectangle(object):
    """ 长方形 """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def area(self):
        return self._x * self._y

if __name__ == '__main__':
    a = Rectangle(1, 2)
    print a.area()
    b = AddHigh(Rectangle, 3)(1, 2)
    print b.area()
    print a.area()
    c=Rectangle(2,3)
    print c.area()