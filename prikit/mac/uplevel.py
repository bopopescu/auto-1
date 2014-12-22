#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry




"""
Usage:
    uplevel.py
    uplevel.py  [-q | --quiet] [-l | --log] [-d | --debug] <filename>
    uplevel.py (-h | --help)
    uplevel.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my uplevel
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






# 遍历所有子目录
# 按目录字母顺序, 子文件顺序, 递归生成文件


def dfs_dir_byplist(root_dir,markdown_file,level,logger=mylog.default_logger()):
    # generate the filelist, ignore the hidden files.

    effective_file=re.compile(r'(^.*_+|^[0-9]*_*)(.*)\.md$')
    plist_file_name=os.path.join(root_dir,'.Ulysses-Group.plist')
    print plist_file_name
    print root_dir, level
    filename_list,dirname_list=get_name_from_plist(plist_file_name)
    print filename_list
    alllists=filename_list+dirname_list
    efflists=[ filename for filename in filename_list if  effective_file.match(filename)]+dirname_list
    print efflists
    # efflists_title=[ effective_file.match(filename).group(2) for filename in alllists if  effective_file.match(filename)]


    #

    for filename in efflists:
        path = os.path.join(root_dir, filename)
        # print logger
        # logger.debug(filename+title)


        # write the file content according to level
        #TODO: 文件夹的处理,文件夹名+.md, .synopsis的处理
        if os.path.isdir(path):
            # markdown_file.write('#'*level+title)
            # markdown_file.write('\n\n')
            # if os.path.exists(str(path)+'/00.content'):
                # markdown_file.write(str(sh.cat(path+'/00.content'))+'\n')
            dfs_dir_byplist(path, markdown_file, level+1)
        else:
            # if title:
                # markdown_file.write('#'*level+title)
            # markdown_file.write('\n\n')
            # markdown_file.write(str(sh.sed('s/^#/'+'#'*level+'#/',path)))
            markdown_file.write(str(sh.sed('s/^#/'+'#'+'/',path)))
            markdown_file.write('\n\n')



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


def walk_sed(dirname):
    md_pattern=re.compile(r'\.md$')
    list_dirs=os.walk(dirname)
    for root,dirs,files in list_dirs:
        for f in files:
            if md_pattern.search(f):

                sh.sed('-i','-e','s/^#//',os.path.join(root, f))

def main(logger=mylog.default_logger()):
    # load arguments and logger
    arguments = docopt(__doc__, version='0.0')
    # print arguments
    # script self name
    self_name=os.path.basename(sys.argv[0])
    # log
    # logfile=self_name.replace('py','log')
    # logger=set_mylogger(arguments,logfile)
    # load config
    # main_config=load_config('.ll')

    # set filename varibles
    # main_title=os.path.basename(os.getcwd())
    # markdown_file_name=os.path.join(os.getcwd(),'build',main_title+'.markdown')
    # docx_file_name=main_title+'.docx'
    # rtf_file_name=main_title+'.rtf'

    md_pattern=re.compile(r'\.md$')

    markdown_file_name=arguments.get('<filename>')
    if markdown_file_name:
        if os.path.isdir(markdown_file_name):
            walk_sed(markdown_file_name)
        else:
            sh.sed('-i','-e','s/^#//',markdown_file_name)
            # sh.sed('-i','-e','s/^#/'+'#/',markdown_file_name)
    else:
        walk_sed('.')


    ## file open operations
    # markdown_file=open(markdown_file_name, 'w')
    # markdown_file.close()
    # sh.open(markdown_file_name)

    # markdown_file=open(markdown_file_name, 'r')

    # mainpart


if __name__ == '__main__':

    main()


