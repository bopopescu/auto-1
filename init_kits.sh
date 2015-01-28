#!/bin/sh
# include all kits path in system paths

kits_path=$HOME/lhrkits/
for dir_name in ` find $kits_path -maxdepth 1 -type d |grep -E  "kit$" `
do
    # echo $dir_name
    source $dir_name/init_kit.sh
done


