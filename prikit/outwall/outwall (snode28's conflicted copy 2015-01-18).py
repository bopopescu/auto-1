#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh
import os
import sys


def outwall():
    try:
        import shadowsocks
    except Exception, e:
        os.system("pip install shadowsocks")
    finally:
        pass

    if sys.platform.find('darwin') != -1:
        try:
            # sh.grep(sh.ps('ux'),'sslocal')
            if not os.popen('ps ux|grep sslocal|grep -v grep').read():
                os.system(
                    "sslocal -c $HOME/lhrkits/prikit/outwall/mac/sslocal_config.json &")
        except Exception, e:
            pass
        finally:

            command_string = ' '.join(sys.argv[1:])
            print command_string
            os.system(
                "$HOME/lhrkits/prikit/outwall/mac/proxychains/proxychains4  -f $HOME/lhrkits/prikit/outwall/mac/proxychains.conf " + command_string)

    elif sys.platform.find('linux') != -1:
        try:
            # sh.grep(sh.ps('ux'),'sslocal')
            if not os.popen('ps ux|grep sslocal|grep -v grep').read():
                os.system(
                    "sslocal -c $HOME/lhrkits/prikit/outwall/linux/sslocal_config.json &")
        except Exception, e:
            pass
        finally:

            command_string = ' '.join(sys.argv[1:])
            print command_string
            os.system(
                "$HOME/lhrkits/prikit/outwall/linux/proxychains/proxychains4  -f $HOME/lhrkits/prikit/outwall/linux/proxychains.conf " + command_string)


def main():
    outwall()

if __name__ == '__main__':
    main()