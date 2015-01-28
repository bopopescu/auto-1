#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh,os,sys

try:
    sh.grep(sh.grep(sh.ps('ux'),'sslocal'),v='grep')
except Exception, e:
    os.system("sslocal -c $HOME/.outwall/sslocal_config.json &")
finally:

    command_string=' '.join(sys.argv[1:])
    print command_string
    os.system("$HOME/.outwall/proxychains-4.8.1/proxychains4  -f $HOME/.outwall/proxychains.conf "+command_string )




