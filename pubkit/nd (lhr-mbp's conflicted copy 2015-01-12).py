#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:
    nd.py [<name>] [-r | --run] [-b | --back] [-q | --quiet] [-l | --log] [-d | --debug]
    nd.py (-h | --help)
    nd.py --version

Options:
    -r --run      run ipython notebook
    -b --back     back to markdown
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

def main(logger=mylog.default_logger()):
    ## load arguments and logger
    arguments = docopt(__doc__, version='0.0')
    ## script self name
    self_name=os.path.basename(sys.argv[0])
    print arguments
    input_name=arguments['<name>']
    pattern=re.compile(r'(.*)\.(.*)$')
    print pattern.match(input_file_name)
    # Rmd_name=name.replace
    # md_name=name.replace()
    run=arguments['--run'] and '--run'
    back=arguments['--back'] and '--back'
    pattern_rmd=re.compile(r'\.Rmd$')
    pattern_md=re.compile(r'\.md$')
    pattern_ipynb=re.compile(r'\.ipynb$')
    if pattern_rmd.search(input_name):
        # cmd="notedown "+ input_name+" --to markdown  --rmagic --knit >"+md_name
        # os.system(cmd)
        # cmd="notedown "+name.replace  --run  >$name.ipynb





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
