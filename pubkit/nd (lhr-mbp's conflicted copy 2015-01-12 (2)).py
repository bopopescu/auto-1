#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:
    nd.py [<name>] [-r | --run] [-b | --back] [--render] [-q | --quiet] [-l | --log] [-d | --debug]
    nd.py (-h | --help)
    nd.py --version

Options:
    -r --run      run ipython notebook
    -b --back     back to markdown
    --render      render
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my nd
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


def md_to_ipynb(md_name, ipynb_name, run):

    cmd = "notedown " + md_name +' '+ run +' >'+ ipynb_name
    print cmd
    if os.path.exists(ipynb_name):
        print "%s is exist, delete it?(y/n)" % (ipynb_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(ipynb_name)
        else:
            sys.exit(0)
    os.system(cmd)


def Rmd_to_md(input_name, md_name):
    cmd = "notedown " + input_name + " --to markdown  --rmagic --knit >" + md_name
    print cmd
    if os.path.exists(md_name):
        print "%s is exist, delete it?(y/n)" % (md_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(md_name)
        else:
            sys.exit(0)
    os.system(cmd)


def ipynb_to_md(input_name, output_md_name, render):
    if render:
        cmd = "notedown " + input_name + r' --to markdown '+render+' >' + output_md_name
    else:
        cmd = "notedown " + input_name + r' --to markdown --stripe >' + output_md_name

    print cmd
    if os.path.exists(output_md_name):
        print "%s is exist, delete it?(y/n)" % (output_md_name),
        yn = raw_input()
        if yn == 'y':
            os.remove(output_md_name)
        else:
            sys.exit(0)
    os.system(cmd)


def ipynb_to_html(input_name, html_name):
    cmd="ipython nbconvert "+input_name +" --to slides --post serve"
    print cmd
    os.system(cmd)


def main(logger=mylog.default_logger()):
    ## load arguments and logger
    arguments = docopt(__doc__, version='0.0')
    ## script self name
    self_name=os.path.basename(sys.argv[0])
    print arguments
    input_name=arguments['<name>']
    pattern=re.compile(r'(.*)\.(.*)$')
    name=pattern.match(input_name).group(1)
    Rmd_name=name+'.Rmd'
    md_name=name+'.md'
    ipynb_name=name+'.ipynb'
    output_md_name=name+'_output.md'
    html_name=name+'.html'
    run=arguments['--run'] and '--run'
    render=arguments['--render'] and '--render'
    back=arguments['--back'] and '--back'
    pattern_rmd=re.compile(r'\.Rmd$')
    pattern_md=re.compile(r'\.md$')
    pattern_ipynb=re.compile(r'\.ipynb$')
    if pattern_rmd.search(input_name):
        Rmd_to_md(input_name, md_name)
        md_to_ipynb(md_name,ipynb_name,run)
    if pattern_md.search(input_name):

        md_to_ipynb(md_name,ipynb_name,run)
        if back:
            ipynb_to_md()
    if pattern_ipynb.search(input_name):
        ipynb_to_md(input_name, output_md_name,render)
        ipynb_to_html(input_name,html_name)


        ## log
    # logfile=self_name.replace('py','log')
    # logger=set_mylogger(arguments,logfile)
    ## load config
    # main_config=load_config('.ll')

    ## set filename varibles
    # dir_name=os.path.basename(os.getcwd())
    # test_file_name='test.txt'
    # test_file=open(test_file_name, 'w')
    # test_file.close()




## mainpart
if __name__ == '__main__':
    main()



#
# if [[ $name =~ \.Rmd$ ]]; then
#     name=${name%.Rmd}
#     # notedown $name.Rmd --run --rmagic --knit >$name.ipynb
#     notedown $name.Rmd --to markdown  --rmagic --knit >$name.md
#     notedown $name.md  --run  >$name.ipynb
# elif [[ $name =~ \.md$ ]]; then
#     name=${name%.md}
#     notedown $name.md --run  >$name.ipynb
# elif [[ $name =~ \.ipynb$ ]]; then
#     name=${name%.ipynb}
#     notedown $name.ipynb --to markdown --render >${name}_output.md
#
# fi


## Usage:
# nd filename.rmd/md --run --back
