#!/bin/sh
# please set kit_dir_name

# 这里不可以用pwd, 因为执行的时候pwd是执行目录, 不是脚本所在目录.
kit_dir_name=${0%/*}

export PATH=$kit_dir_name:$PATH

for dir_name in `find $kit_dir_name -maxdepth 1 -type d |grep -E -v "\./[.].*" | sed '1d'`
do
    # echo $dir_name
    export PATH=$dir_name:$PATH
done
