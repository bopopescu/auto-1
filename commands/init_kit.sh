#!/usr/bin/env bash


kit_dir_name=${0%/*}
export PATH=$kit_dir_name:$PATH

for dir_name in `find $kit_dir_name -maxdepth 1 -type d |grep -E -v "\./[.].*" | sed '1d'`
do
    # echo $dir_name
    export PATH=$dir_name:$PATH
done
