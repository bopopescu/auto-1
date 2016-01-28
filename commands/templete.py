#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry




"""
Usage:

    mytex.py  [-q | --quiet] [-l | --log] [-d | --debug]
    templete.py (-h | --help)
    templete.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my templete
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


def dfs_dir(root_dir,markdown_file,level,logger=mylog.default_logger()):
    # generate the filelist, ignore the hidden files.
    hiden_file=re.compile(r'^\.|main_title\.md|\.synopsis$|\.markdown')
    effective_file=re.compile(r'(^.*_+|^[0-9]*_*)(.*)\.md$')
    efflists=[ filename for filename in os.listdir(root_dir) if  effective_file.match(filename)]
    efflists_title=[ effective_file.match(filename).group(2) for filename in os.listdir(root_dir) if  effective_file.match(filename)]

    alllists=[ filename for filename in os.listdir(root_dir) if not hiden_file.match(filename)]

    #
    for filename,title in zip(efflists,efflists_title):
        path = os.path.join(root_dir, filename)
        # print logger
        logger.debug(filename+title)


        # write the file content according to level
        #TODO: 文件夹的处理,文件夹名+.md, .synopsis的处理
        if os.path.isdir(path):
            markdown_file.write('#'*level+title)
            markdown_file.write('\n')
            # if os.path.exists(str(path)+'/00.content'):
                # markdown_file.write(str(sh.cat(path+'/00.content'))+'\n')
            dfs_dir(path, markdown_file, level+1)
        else:
            if title:
                markdown_file.write('#'*level+title)
            markdown_file.write('\n')
            markdown_file.write(str(sh.sed('s/^#/'+'#'*level+'#/',path)))




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

    # set filename varibles
    main_title=os.path.basename(os.getcwd())
    markdown_file_name=os.path.join(os.getcwd(),'build',main_title+'.markdown')
    docx_file_name=main_title+'.docx'
    rtf_file_name=main_title+'.rtf'


    ## file open operations
    # markdown_file=open(markdown_file_name, 'w')
    # markdown_file.close()
    # sh.open(markdown_file_name)

    # markdown_file=open(markdown_file_name, 'r')

    # mainpart


if __name__ == '__main__':

    main()


