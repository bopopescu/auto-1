#!/bin/sh
# please set kit_dir_name

kit_dir_name=$HOME/lhrkits/prikit/
export PATH=$kit_dir_name:$PATH

for dir_name in `find $kit_dir_name -maxdepth 1 -type d |grep -E -v "\./[.].*" | sed '1d'`
do
    export PATH=$dir_name:$PATH
done


