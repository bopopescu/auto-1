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
    labkitpath=os.path.join(home,'labkit')
    if not labkitpath in sys.path:
        sys.path.append(labkitpath)
    list_dirs=os.walk(labkitpath)
    for root,dirs,files in list_dirs:
        for d in dirs:
            if not d in sys.path:
                sys.path.append(d)


import_labkit_path()


def walk_sed(dirname):
    md_pattern=re.compile(r'\.md$')
    list_dirs=os.walk(dirname)
    for root,dirs,files in list_dirs:
        for f in files:
            if md_pattern.search(f):

                sh.sed('-i','-e','s/^#//',os.path.join(root, f))


def main(logger=mylog.default_logger()):
    arguments = docopt(__doc__, version='0.0')
    self_name = os.path.basename(sys.argv[0])
    # logfile=self_name.replace('py','log')
    # logger=set_mylogger(arguments,logfile)
    # main_config=load_config('.ll')

    # dir_name=os.path.basename(os.getcwd())
    # test_file_name='test.txt'
    # test_file=open(test_file_name, 'w')
    # test_file.close()


if __name__ == '__main__':
    main()


