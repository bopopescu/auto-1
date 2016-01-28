#!/bin/sh
# include all kits path in system paths


for dir_name in ` find $AUTO -maxdepth 1 -type d |grep -E  "kit$" `
do
    # echo $dir_name
    if [ -f $dir_name/init_kit.sh ]; then
        source $dir_name/init_kit.sh
    fi

done
