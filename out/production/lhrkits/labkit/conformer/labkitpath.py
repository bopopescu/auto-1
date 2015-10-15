#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
   import this file can include all labkit py file in system's path
"""

from docopt import docopt
import os, sys, re, sh
from glob import glob
import yaml, logging

import mypub
import crash_on_ipy
import mylog

def import_labkit_path():
    home=os.environ['HOME']
    # print home
    labkitpath=os.path.join(home,'lhrkits/labkit')
    if not labkitpath in sys.path:
        sys.path.append(labkitpath)
    list_dirs=os.walk(labkitpath)
    for root,dirs,files in list_dirs:
        for d in dirs:
            if not d in sys.path:
                sys.path.append(os.path.join(root,d))


import_labkit_path()

