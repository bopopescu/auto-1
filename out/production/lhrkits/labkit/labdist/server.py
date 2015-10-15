#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# from rq import Queue
import time
from redis import Redis
from rq import Queue, use_connection
from labkit.config import REDIS_SERVER,REDIS_PORT

redis_conn = Redis(host=REDIS_SERVER,port=REDIS_PORT)
q = Queue(connection=redis_conn)  # no args implies the default queue

from labkit.metacalc.labqm.gaussian import gaussian, gaussian_conformer

from labkit.conformer.conformer import Conformer


def rq_gaussian(conformer):
    q.enqueue(gaussian,conformer.dumps())



def test():
    coll=Conformer.get_coll('tmp','tmp')
    conformer=coll.Conformer()
    # conformer.collection=get_coll('tmp','ttmp')
    # conformer.set_coll('ttmp','tttmp')
    conformer.load(filename='/Users/lhr/lhrkits/labkit/test/cggg1.xyz')
    # cc=gaussian_conformer(conformer)
    # result = q.enqueue(count_words_at_url, "www.baidu.com")

    # cc.save()

    from labkit.conformer.polypeptide import *

    cc=pep_from_seq('CGGGG')
    # print cc
    # xyz=cc.dumps()
    # print xyz
    # gaussian(xyz)
    # result=q.enqueue(gaussian, xyz)
    rq_gaussian(cc)

    # while True:
    #     s=result.result
    #     if s:
    #         print s
    #         new_c=Conformer().loads(s)
    #         break
    # print new_c.dumps()
    # result = q.enqueue(gaussian, (conformer))

# test()






if __name__ == '__main__':
    pass


