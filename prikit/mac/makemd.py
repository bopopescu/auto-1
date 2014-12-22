#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-01 21:08:02
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
# @Version : $Id$




"""
Usage:
    makemd.py
    makemd.py (-l | --log)
    makemd.py (-q | --quiet)
    makemd.py (-d | --debug)
    makemd.py (-h | --help)
    makemd.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
    分级处理目录, 目录
    模型:
    最外层为文章 title, 内部第一层为章, 第二层为节, 如果用 md文件就可以直接涵盖章节.

    .md 作为基本单元, 分为

    - 目录+.md, 基本单元, 等价于# 目录名 + .md内容
    - 文件.md 基本单元(# 文件名+开头内容)+次级单元(内部的# 作为次级)

    .main文件指定主文件夹以及生成的类型, 在.main 文件内部按行写上

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

def dfs():
   # filename=glob.
    sh.sed('-i','s/^#/##/',filename)

def dfs_dir(root_dir,markdown_file,level,logger=mylog.default_logger()):
    # generate the filelist, ignore the hidden files.
    hiden_file=re.compile(r'^\.|main_title\.md|\.synopsis$|\.markdown')
    effective_file=re.compile(r'(^.*_+|^[0-9]*_*)(.*)\.md$')
    plist_file_name='.Ulysses-Group.plist'
    efflists=[ filename for filename in get_name_from_plist(plist_file_name) if  effective_file.match(filename)]
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
            markdown_file.write('\n\n')
            # if os.path.exists(str(path)+'/00.content'):
                # markdown_file.write(str(sh.cat(path+'/00.content'))+'\n')
            dfs_dir(path, markdown_file, level+1)
        else:
            if title:
                markdown_file.write('#'*level+title)
            markdown_file.write('\n\n')
            markdown_file.write(str(sh.sed('s/^#/'+'#'*level+'#/',path)))
            markdown_file.write('\n\n')

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



from biplist import *
def get_name_from_plist(plist_file_name):

    try:
        plist = readPlist(plist_file_name)
        # print plist
    except (InvalidPlistException, NotBinaryPlistException), e:
        print "Not a plist:", e

    newlist=[ i[0] for i in plist.get('sheetClusters') ]
    filename_list= newlist
    newlist=plist.get('childOrder')
    dirname_list=newlist
    if not filename_list:
        filename_list=[]
    if not dirname_list:
        dirname_list=[]
    return filename_list, dirname_list


def mmd2tex(markdown_file_name,main_title,type,lang):
    if not os.path.exists('latex'):
        sh.mkdir('latex')
    sh.cd('latex')
    if not os.path.exists('images') and os.path.exists('../images'):
        sh.ln('-s','../images','./')

    tex_file_name=main_title+'_'+type+'_'+lang+'.tex'

    # sh.pandoc(markdown_file_name,f="markdown_mmd",t="latex",o=tex_file_name)

    # generate proper tex file
    # main_title=str(sh.sed('-n','s/^# //p',markdown_file_name))
    tmp_markdown_file_name=tex_file_name.replace('.tex','.markdown')
    if type=='report':
        # report_markdown=main_title+'_report.markdown'
        sh.cp(markdown_file_name,tmp_markdown_file_name)
        # sh.sed('-i','-e','s/^#/'+'#/',tmp_markdown_file_name)

        sh.mmd2tex(tmp_markdown_file_name)
        # sh.mv(report_markdown,tex_file_name)
    elif type=='article':
        # article_markdown=main_title+'_article.markdown'
        sh.cp(markdown_file_name,tmp_markdown_file_name)
        sh.sed('-i','-e','s/^#/'+'#'*2+'/',tmp_markdown_file_name)
        sh.mmd2tex(tmp_markdown_file_name)
        # sh.mv(article_markdown.replace(,tex_file_name)
    else:
        return


    tex_file=open(tex_file_name,'r')
    content_list=tex_file.readlines()
    tex_file.close()
    if type=='report' and lang=='cn':
        prefix='''
% -*- coding: utf-8 -*-
\documentclass[UTF8,nofonts]{ctexrep}
\setCJKmainfont[BoldFont=STHeiti,ItalicFont=STKaiti]{STSong}
\setCJKsansfont[BoldFont=STHeiti]{STXihei}
\setCJKmonofont{STFangsong}

'''

    elif type=='article' and lang=='cn':
        prefix='''
% -*- coding: utf-8 -*-
\documentclass[UTF8,nofonts]{ctexart}
\setCJKmainfont[BoldFont=STHeiti,ItalicFont=STKaiti]{STSong}
\setCJKsansfont[BoldFont=STHeiti]{STXihei}
\setCJKmonofont{STFangsong}

'''

    elif type=='article' and lang=='en':
        prefix='''
% -*- coding: utf-8 -*-
\documentclass[UTF8]{article}

'''

    elif type=='report' and lang=='en':
        prefix='''
% -*- coding: utf-8 -*-
\documentclass[UTF8]{report}
'''

    secfix='''
\usepackage{graphicx}

\\begin{document}
\\title{%s} \\author{Haorui Lu}  \maketitle
\\tableofcontents
''' % (main_title)
    surfix='''
\end{document}
'''

    content_list.insert(0,secfix)
    content_list.insert(0,prefix)
    content_list.append(surfix)

    tex_file=open(tex_file_name,'w')
    tex_file.writelines(content_list)
    tex_file.close()
    _s=open(tex_file_name,'r').read().replace('includegraphics{','includegraphics[width=\\textwidth]{')
    open(tex_file_name,'w').write(_s)
    try:
        run_mytex=sh.Command("mytex.py")
        run_mytex(tex_file_name)
    except Exception, e:
        pass
    pdf_file_name=tex_file_name.replace('tex','pdf')
    if os.path.exists(pdf_file_name):
        sh.cd('..')
        if not os.path.exists(pdf_file_name):
            sh.ln('-s',os.path.join('latex',pdf_file_name))
        sh.open(pdf_file_name)


def mmd2rtf(markdown_file_name,rtf_file_name):
    sh.pandoc(markdown_file_name,f="markdown_mmd",t="rtf",o=rtf_file_name)
def mmd2docx(markdown_file_name,docx_file_name):
    sh.pandoc(markdown_file_name,f="markdown_mmd",t="docx",o=docx_file_name)

def add_quotation(s):
    return '\"'+s+'\"'


def main():
    arguments = docopt(__doc__, version='makemd 1.0')
    # print arguments

    # up to root
    if not up_to_main():
        print(".main file not exist, bort. Please creat a .main file in the main folder.")
        return

    main_config=yaml.load(open(".main",'r'))
    if not main_config:
        main_config={}

    if arguments.get('-l') or arguments.get('--log'):
        logger=mylog.set_logger(filename='makemd.log', level=mylog.logging.INFO)
    elif arguments.get('-q') or arguments.get('--quiet'):
        logger=mylog.set_logger(filename='makemd.log', level=mylog.logging.ERROR)
    elif arguments.get('-d') or arguments.get('--debug'):
        logger=mylog.set_logger(filename='makemd.log', level=mylog.logging.DEBUG)
    else:
        logger=mylog.set_logger(level=mylog.logging.INFO)

    logger.debug(arguments)

    # load main_config
    if main_config.has_key('output_type_list'):
        logger.info('output_type_list are %s' % main_config['output_type_list'])
## A .main config file sample. using yaml.
## output_type_list:
##    - latex_article
##    #- latex_report
##    #- rtf
##    #- docx

    # set filename varibles
    main_title=os.path.basename(os.getcwd())
    if not os.path.exists('.build'):
        sh.mkdir('.build')
    sh.cd('.build')
    if not os.path.exists('images') and os.path.exists('../images'):
        sh.ln('-s','../images','./')
    markdown_file_name=os.path.join(os.getcwd(),main_title+'.markdown')
    # markdown_file_name=os.path.join(os.getcwd(),main_title+'.markdown')
    docx_file_name=main_title+'.docx'
    rtf_file_name=main_title+'.rtf'


    # generate main_title.markdown file
    markdown_file=open(markdown_file_name, 'w')
    # markdown_file.write('#'+os.path.basename(os.getcwd())+'\n')
    # sh.cd('..')
    dfs_dir_byplist(os.pardir,markdown_file,0,logger)
    markdown_file.close()
    sh.open(markdown_file_name)

    markdown_file=open(markdown_file_name, 'r')

    if main_config.has_key('output_type_list'):

        # generate latex file
        if main_config['output_type_list'] and ('latex_report' in main_config['output_type_list'] or 'latex_article' in main_config['output_type_list']):
            content=markdown_file.read()
            encoding=chardet.detect(content)['encoding']
            if encoding == 'utf-8' and 'latex_report' in main_config['output_type_list']:
                # generate latex & pdf file by article
                mmd2tex(markdown_file_name,main_title,'report','cn')
            if encoding == 'utf-8' and 'latex_article' in main_config['output_type_list']:
                # generate latex & pdf file by article
                mmd2tex(markdown_file_name,main_title,'article','cn')

            if encoding != 'utf-8' and 'latex_report' in main_config['output_type_list']:
                mmd2tex(markdown_file_name,main_title,'report','en')
            if encoding != 'utf-8' and 'latex_article' in main_config['output_type_list']:
                # generate latex & pdf file by article
                mmd2tex(markdown_file_name,main_title,'article','en')
            logger.info("tex & pdf file generated")


        # generate rtf file
        if  main_config['output_type_list'] and 'rtf' in main_config['output_type_list']:
            mmd2rtf(markdown_file_name,rtf_file_name)
            sh.open(rtf_file_name)
            logger.info("rtf file generated")

        # generate docx file
        if  main_config['output_type_list'] and 'docx' in main_config['output_type_list']:
            mmd2docx(markdown_file_name,docx_file_name)
            sh.open(docx_file_name)
            logger.info("docx file generated")

if __name__ == '__main__':

    main()


