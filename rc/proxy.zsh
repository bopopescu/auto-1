#!/bin/zsh

export http_proxy=`proxy-config -h`
export https_proxy=`proxy-config -s`
export ftp_proxy=`proxy-config -f`
