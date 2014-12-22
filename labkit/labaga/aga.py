__author__ = 'lhr'
import os
import mypub
# import newtest
import pdb, sh


ustc = 1
ustc=2

class A():

    a = ustc
    b = 2


class B():
    a = ustc
    b = 2




a = A()
print vars(a)
print dir(a)


@classmethod
def add(self, a, b):
    print a + b


A.add = add
# A.add=staticmethod(add)
b = B()


# print vars(b)
# print dir(b)
#

# print dir(A)
def ustc_method():
    return ustc


a.add(ustc_method(), 2)

