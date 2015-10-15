#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



import os, sys, re, sh
from glob import glob
import yaml,logging
from labkit.common import smartlog

import mypub, labkitpath
import crash_on_ipy

from Bio.PDB.Structure import *
from Bio.PDB.Polypeptide import *
from Bio.PDB.PDBParser import PDBParser
import math
import StringIO
import tempfile
# import pandas as pd
from copy import deepcopy
import inspect
import numpy
from Bio.PDB import PDBIO
from Bio.PDB.StructureBuilder import StructureBuilder
from Bio.PDB.Vector import *
from conformer import Conformer
from Bio.PDB.NeighborSearch import NeighborSearch

from labkit.common import *

import pandas as pd

from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom


## todo: 这里需要再看一下
def as_method_of(cls):
    def as_method_of_cls(func):
        setattr(cls,func.__name__,func)
    return as_method_of_cls
def as_staticmethod_of(cls):
    def as_method_of_cls(func):
        setattr(cls,func.__name__,staticmethod(func))
    return as_method_of_cls


##### 初始化常量
# MIN_ELEMENT_DISTANCE=0.0;
# H_RADIUS=0.365;
# C_RADIUS=0.885;
# O_RADIUS=0.84;
# N_RADIUS=0.86;
# P_RADIUS=1.22;
# S_RADIUS=1.17;


###### 如果有原子对满足以下两条: 非成键, 间距小于判据[两原子原子半径之和加上允许的原子间空白距离:键长], 则非法
DISTANCE_SEARCH_RANGE=1.6  # 合法性判断的搜索范围, 单位A
MIN_SPACE_DISTANCE=0       # 允许的原子半径之间的空白距离
# 原子半径
ELEMENT_RADIUS_DICT={
    'H':0.365,
    'C':0.885,
    'O':0.84,
    'N':0.86,
    'P':1.22,
    'S':1.17,
}
DEFAULT_RADIUS=0 # 如果不在此表中, 默认值为0


standard_aa_names_sorted=["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS",
                          "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL",
                          "TRP", "TYR"]
standard_aa_names_sorted.sort()


# 肽键判据: 原子为C,N且距离为PEPTIDE_BOND, 误差不超过PEPTIDE_BOND_ERROR. 肽键判据在判断键合关系的时候有用
PEPTIDE_BOND=1.3256437
PEPTIDE_BOND_ERROR = 0.05


# load多肽的时候只考虑标准氨基酸, 默认值为1, 改为0可以处理非标准氨基酸, 可能要检查程序.
ONLY_CONSIDER_STANDARD_AA=1

PI=math.pi

script_folder = reflection.get_script_location(__file__)
all_aa_file_name=os.path.join(script_folder,'all_aa.pdb')


# all_aa_file_name='all_aa_babel.pdb'
#
# def build_template():
#     structure=PDBParser().get_structure('all_aa',all_aa_file_name)
#     # print list(structure.get_atoms())
#     p=PPBuilder()
#     s=p.build_peptides(structure,ONLY_CONSIDER_STANDARD_AA)
#     return s[0]

@as_staticmethod_of(Polypeptide)
def build_from_conformer(cc):
    # todo: 从pdb load进多肽
    # todo: 重命名残基名字的问题
    pdbstring=cc.dumps('pdb')

    # print pdbstring
    atomlist=re.compile(r'^ATOM.*$',re.M).findall(pdbstring)
    pep=Polypeptide()
    # 只能处理12列的情况, 如果pdb不符合则会有bug
    data=pd.DataFrame([i.split() for i in atomlist],columns=['ATOM','ATOM_ID','ATOM_NAME','RES_NAME','CHAIN','RES_ID','X','Y','Z','OCCUPANCY','TEMPFACTOR','ELEMENT'])
    for grouped_res in  data.groupby('RES_ID'):
        res_id= int(grouped_res[1]['RES_ID'].iloc[0])
        res_full_id= (' ',grouped_res[1]['RES_ID'].iloc[0],' ')
        res_name= grouped_res[1]['RES_NAME'].iloc[0]

        # todo: segid is None, 查init_res函数的调用里面的segid怎么设置的
        res=Residue(res_full_id,res_name,None)
        res.res_id=res_id
        if res_name=='SER':
            duplicated_h=False

            for grouped_atom in grouped_res[1].groupby('ATOM_ID'):
                serial_number=grouped_atom[1]['ATOM_ID'].iloc[0]
                element=grouped_atom[1]['ELEMENT'].iloc[0]

                name=grouped_atom[1]['ATOM_NAME'].iloc[0]
                if name=='H':
                    if not duplicated_h:
                        name=grouped_atom[1]['ATOM_NAME'].iloc[0]
                        duplicated_h=True
                    else:
                        name=grouped_atom[1]['ATOM_NAME'].iloc[0]+'HH'
                x=grouped_atom[1]['X'].iloc[0]
                y=grouped_atom[1]['Y'].iloc[0]
                z=grouped_atom[1]['Z'].iloc[0]
                coord=numpy.array((float(x),float(y),float(z)))
                occupancy=grouped_atom[1]['OCCUPANCY'].iloc[0]
                bfactor=grouped_atom[1]['TEMPFACTOR'].iloc[0]

                # 这两个暂时乱填
                fullname=grouped_atom[1]['RES_NAME'].iloc[0],grouped_atom[1]['ATOM_NAME'].iloc[0]
                # @param altloc: alternative location specifier for disordered atoms
                # @type altloc: string
                altloc=''
                atom=Atom(name,coord,bfactor,occupancy,altloc,fullname,serial_number,element)
                atom.res_name=res_name
                atom.res_id=res_id
                res.add(atom)

        else:
            # print list(grouped_res[1]['ATOM_NAME'],)
            for grouped_atom in grouped_res[1].groupby('ATOM_ID'):
                serial_number=grouped_atom[1]['ATOM_ID'].iloc[0]
                element=grouped_atom[1]['ELEMENT'].iloc[0]
                name=grouped_atom[1]['ATOM_NAME'].iloc[0]
                x=grouped_atom[1]['X'].iloc[0]
                y=grouped_atom[1]['Y'].iloc[0]
                z=grouped_atom[1]['Z'].iloc[0]
                coord=numpy.array((float(x),float(y),float(z)))
                occupancy=grouped_atom[1]['OCCUPANCY'].iloc[0]
                bfactor=grouped_atom[1]['TEMPFACTOR'].iloc[0]

                # 这两个暂时乱填
                fullname=grouped_atom[1]['RES_NAME'].iloc[0],grouped_atom[1]['ATOM_NAME'].iloc[0]
                # @param altloc: alternative location specifier for disordered atoms
                # @type altloc: string
                altloc=''
                atom=Atom(name,coord,bfactor,occupancy,altloc,fullname,serial_number,element)
                atom.res_name=res_name
                atom.res_id=res_id
                res.add(atom)

        pep.append(res)
        # print len(pep)

    def get_res_id(res):
        # print res.get_id()[1]
        return int(res.res_id)


    pep.sort(key=get_res_id)
    # print pep
    return pep



def build_template():
    return Polypeptide.build_from_conformer(Conformer().load(all_aa_file_name,'pdb'))

TEMPLATE=build_template()  # 20个标准氨基酸模板肽链

# print TEMPLATE[1].child_list[1].res_name

d3_to_residue={}
d1_to_residue={}
for index in d3_to_index.keys():
    for i in TEMPLATE:
        if i.resname == index:
            matched_residue=i
            break
    d1_to_residue[three_to_one(index)]=matched_residue
    d3_to_residue[index]=matched_residue


############# 构型修饰
def neutralize(pep):
    # todo: 中性化
    pass

@as_method_of(Polypeptide)
def addH3():
    # todo: 补全NH2端
    pass

@as_method_of(Polypeptide)
def addOXH():
    # todo: 补全COOH端
    pass

####### 辅助函数

def atom_list(res):
    "遍历返回一个残基的原子名字和坐标"
    return [(i.get_name(),i.get_coord()) for i in res]


@as_method_of(Polypeptide)
def get_atom_list(self):
    """Get list of C-alpha atoms in the polypeptide.

    @return: the list of C-alpha atoms
    @rtype: [L{Atom}, L{Atom}, ...]
    """
    atom_list=[]
    for res in self:
        for atom in res:
            atom_list.append(atom)
    return atom_list

def axis_rotate_with_start_end(p,start,end,angle):
    "从end-start看去, 对着箭头, 绕着此轴顺时针转动angle"
    # todo: 待再次确认, 测试
    axis=end-start
    angle=angle
    m=rotaxis(angle, axis)
    return (p-start).left_multiply(m)+start


@as_method_of(Vector)
def axis_rotate_with_origin(v,axis,angle):
    m=rotaxis(angle,axis)
    return v.left_multiply(m)


def load_top():
    # todo: 根据角度定义(残基名称, 角度名称: 角度原子) 文件或者top文件获得templete, 键连接关系
    pass

def get_four_atoms(dihedral_name):
    # todo: 根据templete获得指定原子, 返回计算二面角用的四个原子.
    pass

# todo: 计算二面角, 设置二面角, 修改完善适用所有二面角

def calc_coord_from_z(v_dis, v_ang, v_dih, dis, ang, dih):
    #toso: 根据z矩阵信息, 四个原子, 计算最后一个原子对应的坐标
    #求该点的坐标，该点与v_dis距离dis,与v_dis,v_ang构成ang的夹角，以v_dis-v_ang轴，与v_dih构成dih二面角
    # CVECTOR v_gs,v_hs,w,r;
    # if(v_dih.p_online(v_ang,v_dis)) throw dis;
    v_gs=v_ang-v_dis
    v_hs=v_dih-v_dis
    w=v_gs**v_hs.axis_rotate_with_origin(v_gs,-dih)
    r=v_gs.normalized()**dis
    return  r.axis_rotate_with_origin(w,ang)+v_dis

def moving(from_atom, target_atom):
    # todo: moving 把构型某一个原子平移到另一个原子上面, 整体平移.
    pass

def moving_atom(self,atom_serial_number):
    # todo: 操作单个原子的平移
    pass


######### 二面角和构型拼接旋转操作

@as_method_of(Polypeptide)
def get_phi_psi_list(self):
    """Return the list of phi/psi dihedral angles."""
    ppl=[]
    lng=len(self)
    for i in range(0, lng):
        res=self[i]
        try:
            n=res['N'].get_vector()
            ca=res['CA'].get_vector()
            c=res['C'].get_vector()
        except:
            # Some atoms are missing
            # Phi/Psi cannot be calculated for this residue
            ppl.append((None, None))
            res.xtra["PHI"]=None
            res.xtra["PSI"]=None
            continue
        # Phi
        if i>0:
            rp=self[i-1]
            try:
                cp=rp['C'].get_vector()
                phi=calc_dihedral(cp, n, ca, c)
            except:
                phi=None
        else:
            # No phi for residue 0!
            try:
                h1=self[i]['H1'].get_vector()
                h2=self[i]['H2'].get_vector()
                h=(h1+h2)/2.0
                phi=calc_dihedral(h, n, ca, c)
            except:
                phi=None


    # Psi
        if i<(lng-1):
            rn=self[i+1]
            try:
                nn=rn['N'].get_vector()
                psi=calc_dihedral(n, ca, c, nn)
            except:
                psi=None
        else:
            # No psi for last residue!
            try:
                o=self[i]['OXT'].get_vector()
                psi=calc_dihedral(n, ca, c, o)
            except:
                psi=None

        ppl.append(phi)
        ppl.append(psi)
        # Add Phi/Psi to xtra dict of residue
        res.xtra["PHI"]=phi
        res.xtra["PSI"]=psi
    return ppl

# todo: 交叉变异生成新构型可以并行, 用map

@as_method_of(Polypeptide)
def set_dihedral(self,dihedral_template,dihedral):
    "dihedral_template is "

    old=self.get_dihedral(dihedral_template)
    # print old
    new=dihedral*PI/180
    # print new
    delta=new-old
    # print delta
    # print dihedral_template


    i=dihedral_template['residue_number']-1
    lng=len(self)
    res=self[i]

    # print res


    if dihedral_template['dihedral_name'].upper()=='PHI' or dihedral_template['dihedral_name'].upper()=='PSI' :
        try:
            n=res['N'].get_vector()
            ca=res['CA'].get_vector()
            c=res['C'].get_vector()
        except:
            # Some atoms are missing
            # Phi/Psi cannot be calculated for this residue
            # ppl.append((None, None))
            res.xtra["PHI"]=None
            res.xtra["PSI"]=None
            return None




    if dihedral_template['dihedral_name'].upper()=='PHI':
        start=n
        end=ca
        pass_atom=['N','HN','H1','H2','H3','CA']
    elif dihedral_template['dihedral_name'].upper()=='PSI':
        start=ca
        end=c
        rest_atom=['O']


    for p in res:
        if p.name in rest_atom:
            # print p.name
            ans=axis_rotate_with_start_end(p.get_vector(),start,end,delta)
            # print p.coord
            # print ans
            p.coord=ans.get_array()

    for left in range(i+1,lng):
        res=self[left]
        for p in res:
            # print p.name,p.coord
            ans=axis_rotate_with_start_end(p.get_vector(),start,end,delta)
            # print ans
            p.coord=ans.get_array()
            # print p.name,p.coord

    return 0

@as_method_of(Polypeptide)
def moving_pep(pep,residue):
    # todo: 移动到一点

    pass


    # todo: 侧链角度二面角的转换列表

@as_method_of(Polypeptide)
def get_dihedral(self,dihedral_template):
    "dihedral_template is "
    # todo: 处理一些边界问题
    i=dihedral_template['residue_number']-1
    lng=len(self)
    # print self.dumps()
    res=self[i]

    if dihedral_template['dihedral_name'].upper()=='PHI' or dihedral_template['dihedral_name'].upper()=='PSI' :
        try:
            n=res['N'].get_vector()
            ca=res['CA'].get_vector()
            c=res['C'].get_vector()
        except:
            # Some atoms are missing
            # Phi/Psi cannot be calculated for this residue
            # ppl.append((None, None))
            res.xtra["PHI"]=None
            res.xtra["PSI"]=None
            return None
    if dihedral_template['dihedral_name'].upper()=='PHI':
        # Phi
        if i>0:
            rp=self[i-1]
            try:
                cp=rp['C'].get_vector()
                phi=calc_dihedral(cp, n, ca, c)
            except:
                phi=None
        else:
            # No phi for residue 0!
            try:
                h1=self[i]['H1'].get_vector()
                h2=self[i]['H2'].get_vector()
                h=(h1+h2)/2.0
                phi=calc_dihedral(h, n, ca, c)
            except:
                phi=None
        return phi

    if dihedral_template['dihedral_name'].upper()=='PSI':

        # Psi
        if i<(lng-1):
            rn=self[i+1]
            try:
                nn=rn['N'].get_vector()
                psi=calc_dihedral(n, ca, c, nn)
            except:
                psi=None
        else:
            # No psi for last residue!
            try:
                o=self[i]['OXT'].get_vector()
                psi=calc_dihedral(n, ca, c, o)
            except:
                psi=None
        return psi

        # Add Phi/Psi to xtra dict of residue
        # res.xtra["PHI"]=phi
        # res.xtra["PSI"]=psi

@as_method_of(Polypeptide)
def __add__(self,other):
    # todo: 目前只是拼合, 还要做移动+旋转, 注意转换矩阵一定要是正交变换. 保持向量模不变
    # todo: combine 拼接: moving, set_dihedral
    # todo: 拼出来的一定要是合法的才行.
    # todo: 注意这里不是deepcopy, 以后要注意, 出现问题的时候回过来看这里.
    # if not self:
    #     return other
    # if not other:
    #     return self

    # end=self[len(self)-1]
    #
    # front=other[0]

    # print dir(front)
    # print inspect.getargspec(front.transform)
    # print atom_list(end)
    # echo_methods(pep1)
    # for i in pep2:
    #     print i.get_list()
    # rotation=rotmat(Vector(1,0,0), Vector(1, 0, 0))
    # translation=numpy.array((0, 0, 1), 'f')
    # [i.transform(rotation,translation) for i in pep1]
    tmp=Polypeptide()
    tmp.extend(self)
    tmp.extend(other)
    # self.logger.debug(type(self))
    # print "debuggggggggggggggggg"
    return tmp

############# 构型检查

@as_method_of(Polypeptide)
def get_atoms(self):
    for res in self:
        for atom in res:
            yield atom



@as_method_of(Polypeptide)
def bebonding(self,atom1, atom2):
    # todo: 给定两个原子, 判断他们是否有键连接, 可以根据gromacs的itp文件判断.
    if self.is_peptide_bond(atom1,atom2):
        return True
    res1=atom1.get_parent().get_resname()
    res2=atom2.get_parent().get_resname()
    # 检验一下这种用法

    # if res1!=res2:
    #     print [res1,atom1.id,res2,atom2.id] in inter_residue_bonding_template
    if res1==res2 and ([res1,atom1.id,atom2.id] in INNER_RESIDUE_BONDING_TEMPLATE or [res1,atom2.id,atom1.id] in INNER_RESIDUE_BONDING_TEMPLATE) :
        return True
    if res1!=res2 and ([res1,atom1.id,res2,atom2.id] in INTER_RESIDUE_BONDING_TEMPLATE or [res2,atom2.id,res1,atom1.id] in INTER_RESIDUE_BONDING_TEMPLATE) :
        return True
    return False

# todo: 键判断这里还有问题, 需要修改


@as_method_of(Polypeptide)
def is_peptide_bond(self,atom1, atom2):
    "判断两个原子C,N是否成肽键"
    if abs((atom1-atom2)-PEPTIDE_BOND)< PEPTIDE_BOND_ERROR and (atom1.id=='C' and atom2.id=='N' or atom1.id=='N' and atom2.id=='C' ):
        return True


# todo: 二硫键, 氢键
# todo: 检查in_residue_bonding_template:



@as_method_of(Polypeptide)
def extract_inner_bonds(self):
    # todo: 判断构型是否合法
    atoms=list(self.get_atoms())
    # pep.logger.debug(atoms)
    # al = [Atom() for j in range(100)]
    ns = NeighborSearch(atoms)
    count =0
    ll=[]
    for (atom1, atom2) in ns.search_all(DISTANCE_SEARCH_RANGE):
        allowed_distance=ELEMENT_RADIUS_DICT.get(atom1.element,DEFAULT_RADIUS)+ELEMENT_RADIUS_DICT.get(atom2.element,DEFAULT_RADIUS)+MIN_SPACE_DISTANCE
        if atom1-atom2 < allowed_distance and  atom1.get_parent().get_resname()==atom2.get_parent().get_resname()  :
            # todo : 没有链接关系, implement bebonding函数
            # ll.append([standard_aa_names_sorted[atom1.get_full_id()[3][1]-1],atom1.id,standard_aa_names_sorted[atom2.get_full_id()[3][1]-1],atom2.id,atom1-atom2,])
            # 老的
            # ll.append([standard_aa_names_sorted[atom1.get_full_id()[3][1]-1],atom1.id,atom2.id])
            ll.append([atom1.res_name,atom1.id,atom2.id])
            # print atom1.serial_number, atom2.serial_number
            # print count
            count =count +1
            return False
    ll.sort()
    # for i in ll:
    #     print i
    return ll



@as_method_of(Polypeptide)
def is_legit(self,print_not_legit=False):
    "判断构型是否合法, print_not_legit=Trule : 打印不合法的键"
    atoms=list(self.get_atoms())
    # pep.logger.debug(atoms)
    # al = [Atom() for j in range(100)]
    ns = NeighborSearch(atoms)
    count =0
    ll=[]
    for (atom1, atom2) in ns.search_all(DISTANCE_SEARCH_RANGE):
        allowed_distance=ELEMENT_RADIUS_DICT.get(atom1.element,DEFAULT_RADIUS)+ELEMENT_RADIUS_DICT.get(atom2.element,DEFAULT_RADIUS)+MIN_SPACE_DISTANCE
        if atom1-atom2 < allowed_distance and  not self.bebonding(atom1,atom2):
            # todo : 没有链接关系, implement bebonding函数
            ll.append([atom1.res_name,atom1.id,atom2.res_name,atom2.id,atom1-atom2,])
            # ll.append([standard_aa_names_sorted[atom1.get_full_id()[3][1]-1],atom1.id,atom2.id])
            # print atom1.serial_number, atom2.serial_number
            # print count
            count =count +1
            # 这里如果return False, 则略去打印过程
            if not print_not_legit:
                return False
    ll.sort()
    for i in ll:
        print i
    if not count:
        return True
    else:
        return False

############## 构型生成和编码

def pep_from_seq(seq):
    "从序列生成多肽构型"
    # todo: 包括d1_to_residue等在内的list和Polypeptide类型的问题, 要写转换函数和构造函数
    pep=Polypeptide()
    # print type(pep), "haha"
    for i in seq:
        pep=pep.__add__(deepcopy([d1_to_residue[i]]))
    return pep


# 从1111开始转


# todo: 加入判断构型合理性
@as_method_of(Polypeptide)
def generate(self,backbone_template,side_template):
    # todo: 根据模板返回系统法的生成器
    '''把构型转化为二面角列表
    (backbone,side) 由主链和侧链二面角在template里面的取值列表拼合而成.
    '''
    # backbone=get_phi_psi_list(pep)
    # 获得侧链二面角
    # side=get_side(pep)
    # todo: 侧链编码
    backbone=[]
    print backbone_template
    for dihedral_template in backbone_template+side_template:
        Polypeptide.logger.debug( self.get_dihedral(dihedral_template))
        # dihedral=pep.get_dihedral(dihedral_template)*180/PI
        # delta_list=[]
        for i in dihedral_template['dihedral_list']:
            # delta= (dihedral-i) % 360
            # if delta >180:
            #     delta=360-180
            # delta_list.append(delta)

            self.set_dihedral(dihedral_template,i)
            if is_legit(self):
                # todo: 这里需要顺序处理, 是否需要deepcopy
                yield self
                # yield deepcopy(self)
            else:
                continue
        # todo: 重启的时候接续的问题, 持久化状态

        # print delta_list
        # print delta_list.index(min(delta_list))
        # backbone.append(delta_list.index(min(delta_list)))

def decoding(backbone_template,side_template=[]):
    "把二面角列表转化为构型"
    # todo: 把code转化为构型
    pep=[]
    return pep
    pass

@as_method_of(Polypeptide)
def first_code(self,backbone_template,side_template):
    # todo:
    code=[]
    # print side_template
    # print backbone_template+side_template
    for dihedral_template in (backbone_template+side_template):
        # Polypeptide.logger.debug( self.get_dihedral(dihedral_template))
        print dihedral_template
        for i in dihedral_template['dihedral_list']:
            self.set_dihedral(dihedral_template,i)
            print self
            if self.is_legit():
                code.append(dihedral_template['dihedral_list'].index(i))
                break
    return code

@as_method_of(Polypeptide)
def encoding(pep,backbone_template=[],side_template=[]):
    '''把构型转化为二面角列表
    (backbone,side) 由主链和侧链二面角在template里面的取值列表拼合而成.
    '''
    # backbone=get_phi_psi_list(pep)
    # 获得侧链二面角
    # side=get_side(pep)
    # todo: 侧链编码
    backbone=[]

    # print backbone_template
    # 提取主链二面角了\
    for dihedral_template in backbone_template:
        Polypeptide.logger.debug( pep.get_dihedral(dihedral_template))
        dihedral=pep.get_dihedral(dihedral_template)*180/PI
        delta_list=[]
        for i in dihedral_template['dihedral_list']:
            delta= (dihedral-i) % 360
            if delta >180:
                delta=360-180
            delta_list.append(delta)
        # print delta_list
        # print delta_list.index(min(delta_list))
        backbone.append(delta_list.index(min(delta_list)))

    side=[]
    for dihedral_template in side_template:
        Polypeptide.logger.debug( pep.get_dihedral(dihedral_template))
        dihedral=pep.get_dihedral(dihedral_template)*180/PI
        delta_list=[]
        for i in dihedral_template['dihedral_list']:
            delta= (dihedral-i) % 360
            if delta >180:
                delta=360-180
            delta_list.append(delta)
        # print delta_list
        # print delta_list.index(min(delta_list))
        side.append(delta_list.index(min(delta_list)))

    return (backbone,side)

def cross(code1,code2):
    # todo: 交叉两个编码
    "交叉两个编码"
    pass


########### 构型计算和判断重复

def rmsd(pep1,pep2):
    # todo:
    pass


def metacalc(calc_func):
    # todo: 提交到labdist上面去计算
    pass




###########  构型的输入输出和配置
# 主要只提供两个方法, 从conformer build, 以及dumps, 要转回conformer请用conformer().loads(pep.dumps()), 虽然也有快捷实现dump_to_conformer()
@as_method_of(Polypeptide)
def dumps(self):
    "dump to xyz format, 注意只有xyz format"
    output = StringIO.StringIO()
    count=0
    for res in self:
        # print res
        for atom in res:
            count+=1
            x,y,z=atom.get_coord()
            print >>output,  atom.element,x,y,z
    output_string=output.getvalue()
    output_string=str(count)+'\n'+'peptide_to_xyz\n'+output_string
    return output_string


@as_method_of(Polypeptide)
def dump(self,filename):
    "dump to xyz format file"
    file=open(filename,'w')
    # Polypeptide.logger.debug(self.dumps())
    file.write(self.dumps())
    file.close()

@as_method_of(Polypeptide)
def dump_to_conformer(self):
    "dump to conformer"
    return Conformer().loads(self.dumps())



# 废弃, 不使用PDBParser
# def build_peptide_from_conformer(cc):
#     # todo: 从pdb load进多肽
#     # pdb=tempfile.NamedTemporaryFile()
#     pdb=open('tmpfile2.pdb','w')
#     # pdb=StringIO.StringIO()
#     # print pdb.getvalue()
#     pdb.write(cc.dumps('pdb'))
#     # pdb.seek(0)
#     pdb.close()
#     # print pdb.name
#     # todo: 重命名残基名字的问题
#     structure=PDBParser().get_structure('conformer','tmpfile2.pdb')
#     # print '#################',list(structure.get_atoms())
#     p=PPBuilder()
#     s=p.build_peptides(structure)
#     pep=s[0]
#     print pep
#     return pep


from labkit.config import *

##############

def main():
    # logfile=self_name.replace('py','log')
    # logger=set_mylogger(arguments,logfile)
    # main_config=load_config('config.yaml')

    # test_file_name='test.txt'
    # test_file=open(test_file_name, 'w')
    # test_file.close()

    pass
    # print TEMPLATE


    io = PDBIO()
    matched_residue=Structure('')
    # origin_structure=PDBParser().get_structure('another','all_aa.pdb')
    # new_structure=StructureBuilder()
    # new_structure.set_header(origin_structure.get_header)
    # new_structure.init_structure('an')
    # s.init_model('1')
    # new_structure.structure=origin_structure

    # new_structure.init_chain()
    # io.set_structure(new_structure.structure)
    # io.save('out.pdb')
    # open('out.xyz','w').write(pep_to_xyz(TEMPLATE))



if __name__ == '__main__':
    main()

