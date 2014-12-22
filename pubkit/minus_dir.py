#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sh,sys
import crash_on_ipy

# in current dir, minus another dir. Only consider the name of file or dir, despite the type of them. You should provide the absolute or relative dir name.
def minus_dir(for_minus_dir):
    '''
    in current dir, minus another dir. Only consider the name of file or dir, despite the type of them. You should provide the absolute or relative dir name.

    '''
    print 'current dir is ',os.getcwd()
    a=os.listdir('.')
    if not os.path.exists(for_minus_dir):
        print for_minus_dir+' not exists'
        return 0
    b=os.listdir(for_minus_dir)
    for_minus_dir_name=os.path.basename(for_minus_dir)
    for_mv_path='moved_files_'+for_minus_dir_name

    if not os.path.exists(for_mv_path):
        os.mkdir(for_mv_path)


    for file_name in b:
        if os.path.exists(file_name):
            print 'moved file:%(file_name)s to %(for_mv_path)s' % locals()
            sh.mv(file_name,for_mv_path)


def main():

    minus_dir(sys.argv[1])
if __name__ == '__main__':
    main()


