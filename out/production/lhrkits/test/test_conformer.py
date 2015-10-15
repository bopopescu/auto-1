#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest
from labkit.conformer.conformer import *

class TestConformer(unittest.TestCase):
    def setUp(self):
        # individual = connection.gaussian.calc1.Conformer()  # this uses the database "test" and the collection "example"
        self.coll=Conformer.get_coll('gaussian','calc2')
        self.individual = self.coll.Conformer()
        self.individual['from_method'] = 'origin'
        self.individual['xyz'] ='''24
0 1
H	20.800000 7.440000 7.800000
C	20.040000 8.160000 8.090000
H	19.070000 7.680000 7.980000
H	20.260000 9.070000 7.530000
C	20.140000 8.560000 9.560000
O	19.460000 8.000000 10.420000
N	21.140000 9.340000 9.970000
H	21.750000 9.750000 9.290000
C	21.270000 9.810000 11.340000
H	21.270000 8.930000 11.970000
C	22.660000 10.410000 11.460000
H	22.650000 11.320000 10.860000
H	23.360000 9.780000 10.910000
C	23.190000 10.500000 12.890000
O	23.550000 9.470000 13.500000
O	23.210000 11.590000 13.500000
C	20.250000 10.840000 11.830000
O	19.880000 10.750000 13.000000
N	19.730000 11.680000 10.930000
H	20.180000 11.800000 10.030000
C	18.830000 12.770000 11.240000
H	17.970000 12.370000 11.760000
H	19.330000 13.560000 11.810000
H	18.410000 13.130000 10.300000

        '''
        self.individual['energy'] = 100.0

        self.xyz= self.individual['xyz']


    def tearDown(self):
        pass

    def test_get_atom(self):
        print self.individual.get_atoms()
        #
        print rmsd(self.individual,self.individual)
        fetched_conformer=Conformer().init(self.individual.collection.find_one())
        fetched_conformer.get_atoms()


    def test_save(self):
        if self.individual.is_needed_in_pool():
            self.individual.save()

    def test_empty(self):
        self.individual.empty()

    def test_load_and_dump(self):
        print self.individual.dumps()

        self.individual.loads(self.xyz)
        print self.individual.dumps()

        self.individual.load('1.out','out')
        self.individual.dump('new.xyz')
        print self.individual.dumps()


    def test_new_individual(self):


        self.individual=self.coll.find_one()

        self.new_individual=self.coll.Conformer()
        self.new_individual['father']=self.individual['_id']
        self.new_individual['from_method'] = 'origin'
        self.new_individual['xyz'] ='''24
    0 1
    H	20.800000 7.440000 7.800000
    C	20.040000 8.160000 8.090000
    H	19.070000 7.680000 7.980000
    H	20.260000 9.070000 7.530000
    C	20.140000 8.560000 9.560000
    O	19.460000 8.000000 10.420000
    N	21.140000 9.340000 9.970000
    H	21.750000 9.750000 9.290000
    C	21.270000 9.810000 11.340000
    H	21.270000 8.930000 11.970000
    C	22.660000 10.410000 11.460000
    H	22.650000 11.320000 10.860000
    H	23.360000 9.780000 10.910000
    C	23.190000 10.500000 12.890000
    O	23.550000 9.470000 13.500000
    O	23.210000 11.590000 13.500000
    C	20.250000 10.840000 11.830000
    O	19.880000 10.750000 13.000000
    N	19.730000 11.680000 10.930000
    H	20.180000 11.800000 10.030000
    C	18.830000 12.770000 11.240000
    H	17.970000 12.370000 11.760000
    H	19.330000 13.560000 11.810000
    H	18.410000 13.130000 10.300000

        '''

        self.new_individual['energy'] = 13300.0

        # print self.new_individual
        self.new_individual.dump('ttt.pdb','xyz')


if __name__ == '__main__':
    unittest.main()