from mongokit import *
import datetime

connection = Connection()


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
print blogpost
# {'body': u'a body', 'title': u'my title', 'date_creation': datetime.datetime(...), 'rank': 0, 'author': u'me'}
blogpost.save()
print connection.test.blogpost.BlogPost()
newblog = connection.test.newexample.BlogPost()
newblog['body'] = u'a body'
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




