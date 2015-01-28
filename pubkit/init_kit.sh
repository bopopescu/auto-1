#!/bin/sh


kit_dir_name=$HOME/lhrkits/pubkit/
export PATH=$kit_dir_name:$PATH

for dir_name in `find $kit_dir_name -maxdepth 1 -type d |grep -E -v "\./[.].*" | sed '1d'`
do
    export PATH=$dir_name:$PATH
done

alias cp=cp

cp -rf $kit_dir_name/mypub.py ~/anaconda/lib/python2.7
source $kit_dir_name/lhr_alias
