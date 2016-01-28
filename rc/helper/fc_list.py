#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generate the functions and commands list for percol
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# 注意shell有用的只是脚本整体的的标准输入和输出. 这是接口, 而不是函数调用返回值之类的. 注意所有的print都起效, 不要乱打印.

from __future__ import print_function
import os, re

def compare_command_name(x,y):
    '''sort ans by command length and name
    '''
    xx=x.split('\t')[0]
    yy=y.split('\t')[0]

    if len(xx)>len(yy):
        return 1
    elif len(xx)<len(yy):
        return -1
    elif len(xx)==len(yy) and xx<yy:
        return -1
    else:
        return 1
def list_fc():
    '''list functions and commands
    '''
    ans=[]
    # # list functions and descriptions in $AUTO/rc/afp.sh
    afp=os.path.join(os.environ['AUTO'],'rc/afp.sh')
    with open(afp) as afp:
        s=afp.read()
        function_pattern=re.compile(r'^\s*function *(.*?)[({]',re.M)
        desc_pattern=re.compile(r'^\s*function .*\n(.*)\n',re.M)
        commands=function_pattern.findall(s)
        desc=desc_pattern.findall(s)
        for i,j in zip(commands,desc):
            ans.append( i+'\t'+j+'\n')



    ignore_pattern=re.compile(r'(\.pyc$)')

    # list commands and descriptions in $AUTO/commands
    commands_dir=os.path.join(os.environ['AUTO'],'commands')
    files=os.listdir(commands_dir)
    for file in files:
        if os.path.isfile(os.path.join(commands_dir,file)) and (not ignore_pattern.search(file)):
            command=file
            try:
                description=open(os.path.join(commands_dir,file)).readlines()[2].strip()
            except:
                description=''
            ans.append(command+'\t'+description+'\n')

    return ''.join(sorted(ans,compare_command_name))


if __name__ == '__main__':
    print(list_fc())
