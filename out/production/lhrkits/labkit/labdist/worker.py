#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

#!/usr/bin/env python
import sys
from rq import Queue, Connection, Worker
from redis import Redis

# Preload libraries
# import library_that_you_want_preloaded

# Provide queue names to listen to as arguments to this script,
# similar to rqworker

from labkit.config import REDIS_SERVER,REDIS_PORT

redis_conn = Redis(host=REDIS_SERVER,port=REDIS_PORT)

with Connection(redis_conn):
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()

if __name__ == '__main__':
    pass


