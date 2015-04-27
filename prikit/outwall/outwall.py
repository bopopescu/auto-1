#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

# important! pliase
outwall_dir="$HOME/lhrkits/prikit/outwall/"



def outwall():
    try:
        import shadowsocks
    except Exception, e:
        os.system("pip install shadowsocks")
    finally:
        pass

    if sys.platform.find('darwin')!=-1:
        try:
            # sh.grep(sh.ps('ux'),'sslocal')
            if not os.popen('ps ux|grep sslocal|grep -v grep').read():
                os.system("sslocal -c "+outwall_dir+"mac/sslocal_config.json &")
        except Exception, e:
            pass
        finally:

            command_string=' '.join(sys.argv[1:])
            print command_string
            os.system(outwall_dir+"/mac/proxychains/proxychains4  -f "+outwall_dir+"mac/proxychains.conf "+command_string )

    elif sys.platform.find('linux')!=-1:
        try:
            # sh.grep(sh.ps('ux'),'sslocal')
            if not os.popen('ps ux|grep sslocal|grep -v grep').read():
                os.system("sslocal -c "+outwall_dir+"linux/sslocal_config.json &")
        except Exception, e:
            pass
        finally:

            command_string=' '.join(sys.argv[1:])
            print command_string
            os.system(outwall_dir+"linux/proxychains/proxychains4  -f "+outwall_dir+"/linux/proxychains.conf "+command_string )

def main():
    outwall()

if __name__ == '__main__':
    main()
