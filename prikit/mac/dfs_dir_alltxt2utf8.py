#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry




"""
Usage:

    dfs_dir.py  [-q | --quiet] [-l | --log] [-d | --debug]
    dfs_dir.py (-h | --help)
    dfs_dir.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my dfs_dir
"""



from docopt import docopt
import mypub
import crash_on_ipy
import os,sys,re
import sh
from glob import glob
import yaml
import chardet
import logging
import mylog



# 回溯到根目录, 找到.main则返回 Ture, 否则返回 False.
def up_to_main():
    if (os.getcwd()== '/'):
        return False
    elif os.path.exists('.main'):
        return True
    else:
        sh.cd('..')
        return up_to_main()
    # return True



# 遍历所有子目录
# 按目录字母顺序, 子文件顺序, 递归生成文件


def dfs_dir(root_dir, re_effective_file, cmd, logger=mylog.default_logger()):
    # generate the filelist, ignore the hidden files.

    # efflists=[ filename for filename in os.listdir(root_dir) if  re_effective_file.match(filename)]

    alllist=os.listdir(root_dir)
    for filename in alllist:
        path = os.path.join(root_dir, filename)


        # write the file content according to level
        #TODO: 文件夹的处理,文件夹名+.md, .synopsis的处理
        if os.path.isdir(path):
            print path
            dfs_dir(path, re_effective_file, cmd)
        elif re_effective_file.match(filename):
            os.system(cmd +' ' +'\"'+path+'\"')



def set_mylogger(arguments,logfile):
    if arguments.get('-l') or arguments.get('--log'):
        logger=mylog.set_logger(filename=logfile, level=mylog.logging.INFO)
    elif arguments.get('-q') or arguments.get('--quiet'):
        logger=mylog.set_logger(filename=logfile, level=mylog.logging.ERROR)
    elif arguments.get('-d') or arguments.get('--debug'):
        logger=mylog.set_logger(filename=logfile, level=mylog.logging.DEBUG)
    else:
        logger=mylog.set_logger(level=mylog.logging.INFO)

    logger.debug(arguments)
    return logger

def load_config(filename='.main',mode='r'):
    """
    A config file sample. using yaml.
    output_type_list:
       - latex_article
       #- latex_report
       #- rtf
       #- docx
   """

    try:
       main_config=yaml.load(open(filename,mode))
    except Exception, e:
       return {}
    if not main_config:
        main_config={}
    return main_config




def main(logger=mylog.default_logger()):
    # load arguments and logger
    arguments = docopt(__doc__, version='0.0')
    # script self name
    self_name=os.path.basename(sys.argv[0])
    # log
    logfile=self_name.replace('py','log')
    logger=set_mylogger(arguments,logfile)
    # load config
    # main_config=load_config('.ll')

    pattern=r'.*\.txt'

    cmd='all2utf8.py'
    re_effective_file=re.compile(pattern)
    dfs_dir('.',re_effective_file,cmd)

    ## file open operations
    # markdown_file=open(markdown_file_name, 'w')
    # markdown_file.close()
    # sh.open(markdown_file_name)

    # markdown_file=open(markdown_file_name, 'r')

    # mainpart


if __name__ == '__main__':

    main()


