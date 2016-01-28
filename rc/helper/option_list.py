#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generate the list which the c cmmand needed.
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# from __future__ import print_function
import os, re

# from list_fc import list_fc
# ans=list_fc()
ans=""
ans="fc\t # list functions and commands\n"+ans
ans="cdto\t # cd to commands folder\n"+ans
ans="delete\t # delete functions and  commands\n"+ans
ans="edit\t # edit functions and  commands\n"+ans
ans="create\t # create new command\n"+ans
ans="afp.sh\t # config the afp.sh\n"+ans
# ans="copy\t # copy\n"+ans

print ans
