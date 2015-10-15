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


from labkit.conformer.polypeptide import check_config,Polypeptide

check_config()

from labkit.conformer.polypeptide import *
print SEQ


class TestPeptide(unittest.TestCase):

    def setUp(self):
        # 测试pep_from_seq & encoding
        # 以及load
        # todo: config 的namespace的问题.
        self.logger=smartlog.get_logger(level="DEBUG")

        # mylog.set_root_logger(level=20)
        # check_config(self.config)
        # structure=PDBParser().get_structure('conformer','all_aa.pdb')
        print SEQ

        self.cc=Conformer()
        # self.cc.load_from_file('all_aa.pdb','pdb')
        self.seq='C'
        self.pep=pep_from_seq(self.seq)
        # print type(self.pep)
        # self.pep=TEMPLATE
        # print TEMPLATE

    def tearDown(self):
        smartlog.clear_logger(self.logger)

    def test_is_legit(self):
        # print self.pep
        print self.pep.is_legit()
        print self.pep.is_legit(1)


    def test_extract_bonds(self):
        # print self.pep
        print self.pep.extract_inner_bonds()

    def test_main(self):
        main()

        self.logger.debug("hahahh")
        # logging.info("hahahh")
    def test_log(self):
        self.logger.debug("haha")
        # logging.info("haha")
        print reflection.get_script_name(__file__)



    def test_encoding(self):
        # code=encoding(self.pep,self.backbone_template)
        # Polypeptide.logger.debug(Conformer().loads(self.pep.dumps()).dump('test.pdb','pdb'))
        # print Conformer.loads(self.pep.dumps())
        cc=Conformer().load("1.xyz")
        # print cc
        self.pep=Polypeptide.build_from_conformer(cc)
        code=self.pep.encoding(BACKBONE_TEMPLATE)
        firstcode=self.pep.first_code(BACKBONE_TEMPLATE,SIDE_TEMPLATE)
        print firstcode

    def test_combine(self):


        pep1=TEMPLATE[:10]
        pep2=TEMPLATE[10:]
        pep1+pep2
    def test_vector(self):

        start=Vector(0,0,0)
        end=Vector(0,0,1)
        angle=PI/3
        p=Vector(0,1,0)

        # should be <Vector -0.87, 0.50, 0.00>
        print axis_rotate_with_start_end(p,start,end,angle)
        # should be <Vector -0.87, 0.50, 0.00>
        print p.axis_rotate_with_origin(end,angle)

        # should be (1,1,0)
        print calc_coord_from_z(p,start,end,1,PI/2,PI/2)
        # print "##############", axis_rotate(p,start,end,angle)


    def test_loads(self):
        self.cc.load('template_test.xyz3')
        # print TEMPLATE[1].segid
        self.pep=Polypeptide.build_from_conformer(self.cc)
        print self.pep.dumps()



    def test_template_and_load_dump(self):
        # todo: 格式不对, 或者空文件, 会卡住
        self.logger.debug(self.pep)
        print 'hello', self.pep
        self.pep.dump('template_text2.xyz')
        self.cc.load('template_test2.xyz','xyz')
        print self.cc.dumps()
        self.cc.loads(TEMPLATE.dumps())
        self.cc.dump('template_test3.xyz')
        self.cc.dump('template_test.pdb','pdb')
        self.pep=Polypeptide()
        self.pep=Polypeptide.build_from_conformer(self.cc)
        print self.pep.dumps()
        self.pep.dump('template_test2.xyz')

    def test_add(self):
        self.pep1=pep_from_seq('C')
        self.pep2=pep_from_seq('GG')
        print self.pep1.get_ca_list()
        print (self.pep1+self.pep2).get_ca_list()
        print self.pep1.get_ca_list()
        print self.pep2.get_ca_list()



    def test_set_dihedral(self):

        # 测试set_dihedral
        # open('cggg1.xyz','w').write(self.pep.dumps())
        # self.pep=pep_from_seq(self.seq)
        cc=Conformer().load("1.xyz")
        print cc
        self.pep=Polypeptide.build_from_conformer(cc)
        self.pep=self.pep+[]
        print self.pep
        self.pep.set_dihedral(BACKBONE_TEMPLATE[0],60)

        open('2.xyz','w').write(self.pep.dumps())



if __name__ == '__main__':
    unittest.main()