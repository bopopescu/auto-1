#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from mongokit import *
import datetime

import labkitpath

import tempfile,sh

connection = Connection()




@connection.register
class Conformer(Document):


    structure = {
        '_type':basestring,
        'from_method' : basestring,
        'from_parameters' : basestring,
        'out_parameters' : basestring,
        'xyz' : basestring,
        'energy' : float,
        'father' : basestring,
        # self.calc_fun=''


    }
    indexes = [
        {
            'fields':['energy'],
        },
    ]
    required_fields = ['from_method', 'xyz', 'energy']
    default_values = {'from_method' : 'origin','from_parameters':'','out_parameters':'', 'father':''}

    def new(self,xyz):
        pass



    def load_from_file(self,filename):
        file=open(filename)
        self['xyz']=file.read()
        self['from_method']='origin'
        self['energy']=0.0


    def set_coll(self,db_name,coll_name):
        '''set the correct collection by db name and collection name'''
        self.collection=connection.__getattr__(db_name).__getattr__(coll_name)
        self.db=connection.__getattr__(db_name)
        # self.collection=get_coll(db_name,coll_name)
        # self.collection=get_coll(db_name,coll_name)
        # self.db=db_name

    # def __init__(self):
    #     super(Conformer, self).__init__()

    @classmethod
    def get_coll(self,db_name,coll_name):
        '''get the correct collection by db name and collection name'''
        coll=connection.__getattr__(db_name).__getattr__(coll_name)
        return coll

    def get_pdb(self):


        xyz_file= tempfile.NamedTemporaryFile()
        pdb_file = tempfile.NamedTemporaryFile()
        xyz_file.write(self['xyz'])
        xyz_file.seek(0)
        # print xyz_file.read()
        # command="babel -ixyz xyz_file.name "
        # print pdb_file.name
        sh.babel("-ixyz",xyz_file.name,"-opdb",pdb_file.name)
        pdb_file.seek(0)
        pdb= pdb_file.read()
        xyz_file.close()
        pdb_file.close()
        return pdb

    def get_xyz(self):
        return self['xyz']
    def get_zmatrix(self):
        xyz_file= tempfile.NamedTemporaryFile()
        zmatrix_file = tempfile.NamedTemporaryFile()
        xyz_file.write(self['xyz'])
        xyz_file.seek(0)
        # print xyz_file.read()
        # command="babel -ixyz xyz_file.name "
        # print pdb_file.name
        sh.babel("-ixyz",xyz_file.name,"-ogzmat",zmatrix_file.name)
        zmatrix_file.seek(0)
        zmatrix= zmatrix_file.read()
        xyz_file.close()
        zmatrix_file.close()
        return zmatrix

    def load_from_zmatrix(self,zmatrix):
        xyz_file= tempfile.NamedTemporaryFile()
        zmatrix_file = tempfile.NamedTemporaryFile()
        zmatrix_file.write(zmatrix)
        zmatrix_file.seek(0)
        # print xyz_file.read()
        # command="babel -ixyz xyz_file.name "
        # print pdb_file.name
        sh.babel("-igzmat",zmatrix_file.name,"-oxyz",xyz_file.name,'-c')
        xyz_file.seek(0)
        xyz= xyz_file.read()
        xyz_file.close()
        zmatrix_file.close()
        self['xyz']= xyz



    def get_father(self):
        if self['father']:
            return self.collection.find({_id:self['father']})
        else:
            return None


def test2():
    pass




def test():

    # individual = connection.gaussian.calc1.Conformer()  # this uses the database "test" and the collection "example"

    coll=get_coll('gaussian','calc2')
    individual = coll.Conformer()
    individual['from_method'] = 'origin'
    individual['xyz'] ='''24
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

    individual['energy'] = 100.0

    individual.save()

    print individual

    individual=coll.find_one()

    new_individual=coll.Conformer()
    new_individual['father']=individual['_id']
    new_individual['from_method'] = 'origin'
    new_individual['xyz'] ='''24
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

    new_individual['energy'] = 13300.0

    print new_individual



if __name__ == '__main__':
    test()

