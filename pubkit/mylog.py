#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
def set_root_logger():
    filename=os.path.basename(__file__)+'.rootlog'

    logging.basicConfig(filename=filename, level = logging.WARN, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')


def default_logger():
    logger=set_logger(level=logging.WARN)
    return logger

def set_logger(logname='mylog', console=True, filename=False,level = logging.DEBUG,filemode='w'):



    # 创建一个logger
    logger = logging.getLogger(logname)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    if filename:
        # 创建一个handler，用于写入日志文件

        # filename=os.path.basename(__file__)+'.log'
        # print filename
        fh = logging.FileHandler(filename,mode=filemode)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if console:
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

mylog=set_logger
def main():
    logger=set_logger(logname="mylog",filename=False, level=logging.DEBUG)
    # set_root_logger()
    # logger.debug('ccd')

if __name__ == '__main__':
    main()


