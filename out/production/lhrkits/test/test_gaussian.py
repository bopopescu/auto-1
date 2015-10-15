#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


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

import unittest
import random
from labkit.common import reflection, smartlog

from labkit.conformer.polypeptide import *
print SEQ

from labkit.metacalc.labqm.gaussian import gaussian


class Testgaussian(unittest.TestCase):

    def setUp(self):
        # 载入测试样例
        # todo: config 的namespace的问题.
        self.logger=smartlog.get_logger(level="DEBUG")


        self.cc=Conformer()
        # self.cc.load_from_file('all_aa.pdb','pdb')
        self.seq='C'
        self.pep=pep_from_seq(self.seq)
        self.cc.loads(self.pep.dumps())
        print self.cc.dumps()
        # print type(self.pep)
        # self.pep=TEMPLATE
        # print TEMPLATE

    def tearDown(self):
        smartlog.clear_logger(self.logger)

    def test_gaussian(self):
        new=gaussian(self.cc)
        print new



if __name__ == '__main__':
    unittest.main()