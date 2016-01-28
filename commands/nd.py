#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:
    nd.py [<name>] [-r | --run] [-j | --json] [--render] [-q | --quiet] [-l | --log] [-d | --debug]
    nd.py (-h | --help)
    nd.py --version

Options:
    -r --run      run ipython notebook
    -j --json     back to markdown
    --render      render
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   nd.py 接 md 文件输出到 ipynb, 接 ipynb 文件返回到 md,
   接 --json 和 --render 参数输出相应的输出md, --run 执行 ipynb

   ref: https://github.com/aaren/notedown
"""

## originmodule
from docopt import docopt
import os,sys,re,sh
from glob import glob
import yaml,logging

## mymodule
import mypub,labkitpath
import crash_on_ipy
import mylog


def md_to_ipynb(md_name, ipynb_name, run_flag):

    cmd = "notedown " + md_name +' '+ run_flag +' >'+ ipynb_name
    print cmd
    if os.path.exists(ipynb_name):
        print "%s is exist, delete it?(y/n)" % (ipynb_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(ipynb_name)
            os.system(cmd)


def Rmd_to_md(input_name, md_name):
    cmd = "notedown " + input_name + " --to markdown  --rmagic --knit >" + md_name
    print cmd
    if os.path.exists(md_name):
        print "%s is exist, delete it?(y/n)" % (md_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(md_name)
            os.system(cmd)


def ipynb_to_json_md(ipynb_name, json_md_name):
    cmd = "notedown " + ipynb_name + r' --to markdown  >' + json_md_name
    print cmd
    if os.path.exists(json_md_name):
        print "%s is exist, delete it?(y/n)" % (json_md_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(json_md_name)
            os.system(cmd)

def ipynb_to_render_md(ipynb_name, render_md_name):
    cmd = "notedown " + ipynb_name + r' --to markdown --render >' + render_md_name
    print cmd
    if os.path.exists(render_md_name):
        print "%s is exist, delete it?(y/n)" % (render_md_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(render_md_name)
            os.system(cmd)


def ipynb_to_html(input_name, html_name):
    cmd="ipython nbconvert "+input_name +" --to html --post serve"
    print cmd
    os.system(cmd)


def get_arg(arguments,arg):
    run_flag = arguments[arg]
    if not run_flag:
        run_flag = ''
    else:
        run_flag = arg
    return run_flag


def ipynb_to_md(ipynb_name, md_name):
    cmd = "notedown " + ipynb_name  +' --to markdown --strip >'+ md_name
    print cmd
    if os.path.exists(md_name):
        print "%s is exist, mv it in %s.bak?(y/n)" % (md_name,md_name),
        yn = raw_input()
        if yn == 'y':
            # os.remove(md_name)
            sh.mv(md_name,md_name+'.bak')
            os.system(cmd)



def main(logger=mylog.default_logger()):
    ## load arguments and logger
    arguments = docopt(__doc__, version='0.0')
    ## script self name
    self_name=os.path.basename(sys.argv[0])
    # print arguments
    input_name=arguments['<name>']
    pattern=re.compile(r'(.*)\.(.*)$')
    name=pattern.match(input_name).group(1)
    Rmd_name=name+'.Rmd'
    md_name=name+'.md'
    ipynb_name=name+'.ipynb'
    json_md_name=name+'_json.md'
    render_md_name=name+'_render.md'
    html_name=name+'.html'
    run_flag = get_arg(arguments,'--run')
    render_flag=get_arg(arguments,'--render')
    json_flag=get_arg(arguments,'--json')

    pattern_rmd=re.compile(r'\.Rmd$')
    pattern_md=re.compile(r'\.md$')
    pattern_ipynb=re.compile(r'\.ipynb$')
    if pattern_rmd.search(input_name):
        Rmd_to_md(input_name, md_name)
        md_to_ipynb(md_name,ipynb_name,run_flag)

    elif pattern_md.search(input_name):
        md_to_ipynb(md_name,ipynb_name,run_flag)

    elif pattern_ipynb.search(input_name):
        ipynb_to_md(ipynb_name,md_name)
        # ipynb_to_html(ipynb_name,html_name)
    else:
        print "please input a .md/Rmd or .ipynb file with option --json or --render"
        sys.exit(0)
    if json_flag:
        ipynb_to_json_md(ipynb_name, json_md_name)
    if render_flag:
        ipynb_to_render_md(ipynb_name,render_md_name)





## mainpart
if __name__ == '__main__':
    main()



