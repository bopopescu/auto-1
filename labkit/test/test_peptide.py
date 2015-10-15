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
from labkit.labkit.conformer.polypeptide import *
from labkit.labkit.common import debugger

class TestPeptide(unittest.TestCase):

    def setUp(self):
        # 测试pep_from_seq & encoding
        # 以及load
        self.config=yaml.load(open('config.yaml','r'))
        self.logger=debugger.get_logger(level="DEBUG")
        # mylog.set_root_logger(level=20)
        # check_config(self.config)
        # structure=PDBParser().get_structure('conformer','all_aa.pdb')

        self.backbone_template=self.config['backbone_template']

        self.cc=Conformer()
        self.cc.load_from_file('all_aa.pdb','pdb')
        self.seq='CGGG'
        self.pep=pep_from_seq(self.seq)
        self.pep=TEMPLATE

    def tearDown(self):
        mylog.clear_logger(self.logger)
    def test_main(self):
        main()
        self.logger.debug("hahahh")
        # logging.info("hahahh")
    def test_log(self):
        self.logger.debug("haha")
        # logging.info("haha")
        print get_script_name(__file__)

    def test_load(self):


        pep=[]
        # load(pep,cc)
        print pep

    def test_encoding(self):
        code=encoding(self.pep,self.backbone_template)
        print code

    def test_combine(self):


        pep1=TEMPLATE[:10]
        pep2=TEMPLATE[10:]
        combine(pep1,pep2)

    def test_vector(self):

        start=Vector(0,0,0)
        end=Vector(0,0,1)
        angle=PI/3
        p=Vector(0,1,0)

        # print "##############", axis_rotate(p,start,end,angle)


    def test_set_dihedral(self):

        # 测试set_dihedral
        open('cggg1.xyz','w').write(pep_to_xyz(self.pep))
        # print pep_to_xyz(self.pep)

        set_dihedral(self.pep,self.backbone_template[0],60)

        open('cggg2.xyz','w').write(pep_to_xyz(self.pep))

#
# class TestSequenceFunctions2(unittest.TestCase):
#
#     def setUp(self):
#         self.seq = range(10)
#
#     def test_shuffle(self):
#         # make sure the shuffled sequence does not lose any elements
#         random.shuffle(self.seq)
#         self.seq.sort()
#         self.assertEqual(self.seq, range(10))
#
#         # should raise an exception for an immutable sequence
#         self.assertRaises(TypeError, random.shuffle, (1, 2, 3))
#
#     def test_choice(self):
#         element = random.choice(self.seq)
#         self.assertTrue(element in self.seq)
#
#     def test_sample(self):
#         with self.assertRaises(ValueError):
#             random.sample(self.seq, 20)
#         for element in random.sample(self.seq, 5):
#             self.assertTrue(element in self.seq)



if __name__ == '__main__':
    unittest.main()