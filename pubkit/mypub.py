#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os,sys

def mypub():
    home=os.environ['HOME']
    mypub=os.path.join(home,'lhrkits/pubkit')
    if not mypub in sys.path:
        sys.path.append(mypub)

mypub()





def import_path(path):

    mypub=path
    if not mypub in sys.path:
        sys.path.append(mypub)



def myimport_single(mymodule):

    home=os.environ['HOME']
    mypub=os.path.join(home,'.yadr/mybin/pub')
    print mypub
    if not mypub in sys.path:
        sys.path.append(mypub)
    if  mymodule in sys.modules:
        mymodule = __import__(mymodule)
    else:
        exec 'import '+mymodule

        mymodule = eval('reload(%s)' % (mymodule))
    return mymodule

def myimport_multi(mymodules):
    for mymodule in mymodules:
        myimport_single(mymodule)

def myimport(mod):
    if type(mod) is list:
        myimport_multi(mod)
    elif type(mod) is str:
        myimport_single(mod)

## codes blow are for notes, not use them!!
# def myimport_single(mymodule):

#     home=os.environ['HOME']
#     mypub=os.path.join(home,'.yadr/mybin/pub')
#     print mypub
#     if not mypub in sys.path:
#         sys.path.append(mypub)
#     if  mymodule in sys.modules:
#         mymodule = __import__(mymodule)
#     else:
#         exec 'import '+mymodule

#         mymodule = eval('reload(%s)' % (mymodule))
#     return mymodule

# def myimport_multi(mymodules):
#     for mymodule in mymodules:
#         myimport_single(mymodule)

# def myimport(mod):
#     if type(mod) is list:
#         myimport_multi(mod)
#     elif type(mod) is str:
#         myimport_single(mod)


if __name__ == '__main__':
    pass