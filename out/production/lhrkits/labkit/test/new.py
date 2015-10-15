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

from docopt import docopt
import os, sys, re, sh
from glob import glob
import yaml, logging

import mypub, labkitpath
import crash_on_ipy
import mylog

print 123
import random
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
    print "h"
    print random.random()

    pool = set(["foo", "bar", "baz", "123", "456", "789"]) # your 240 elements here
    slen = len(pool) / 3 # we need 3 subsets
    set1 = set(random.sample(pool, slen)) # 1st random subset
    pool -= set1
    set2 = set(random.sample(pool, slen)) # 2nd random subset
    pool -= set2
    set3 = pool # 3rd random subset
    # print set1,set2,set3


if __name__ == '__main__':
    main()


