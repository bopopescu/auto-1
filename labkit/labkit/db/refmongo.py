#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from mongokit import *
import datetime

import labkitpath


connection = Connection()

# connection.register([Labconformer])

def push():
    pass





@connection.register
class Conformer():


    structure = {
        'from_method' : basestring,
        'from_parameters' : basestring,
        'out_parameters' : basestring,
        'xyz' : basestring,
        'energy' : float,
        'father' : basestring,
        'rank': int
        # self.calc_fun=''
    }
    indexes = [
        {
            'fields':['energy', ''],
            'unique':True,
        },
    ]
    required_fields = ['from_method', 'xyz', 'energy']
    default_values = {'from_parameters':'','out_parameters':'', 'father':''}

@connection.register
class BlogPost(Document):
    structure = {
        'title': unicode,
        'body': unicode,
        'author': unicode,
        'date_creation': datetime.datetime,
        'rank': int
    }

    required_fields = ['title', 'author', 'date_creation']
    default_values = {'rank': 0, 'date_creation': datetime.datetime.utcnow}


blogpost = connection.test.example.BlogPost()  # this uses the database "test" and the collection "example"
blogpost['title'] = u'my title'
blogpost['body'] = u'a body'
blogpost['author'] = u'me'
# blogpost.author = u'me'

print blogpost
# {'body': u'a body', 'title': u'my title', 'date_creation': datetime.datetime(...), 'rank': 0, 'author': u'me'}

import time

#
# conformer用一样的, 每个用不同的db,手动继承conformer的接口!
# metacalc也和conformer统一起来, 然后接受字典. 只修改相应的项.

start = time.clock()

def mongokit_test():
    for i in range(1):
        blogpost.save()

mongokit_test()

elapsed = (time.clock() - start)
print("Time used:",elapsed)

start = time.clock()


mongokit_test()

elapsed = (time.clock() - start)
print("Time used:",elapsed)

print connection.test.blogpost.BlogPost()
newblog = connection.test.newexample.BlogPost()
# newblog['body'] = u'a body'
newblog['author'] = u'me'
newblog['title'] = u'my new title'
newblog.save()

import mypub
import crash_on_ipy

for post in connection.test.newexample.find():
    print post['title']

print connection.test.newexample.find_random()
# print connection.test.newexample.find().next()
# print connection.test.newexample.find().next()

@connection.register
class ComplexDoc(Document):
    __database__ = 'test'
    __collection__ = 'example'
    structure = {
        "foo": {"content": int},
        "bar": {
            'bla': {'spam': int}
        }
    }


required_fields = ['foo.content', 'bar.bla.spam']




