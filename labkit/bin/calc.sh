#!/bin/sh
op=`dirname $1`
workingfile=`basename $1`
mkdir /local/tmp


if [ `grep -c pm3 $1` -gt 0 ]
then
  cd /dev/shm && cp $op/$workingfile . && metacalc $workingfile
  mv ${workingfile%.*}.* $op/ && rm $op/$workingfile; cd $op;
else
  cd /local/tmp && cp $op/$workingfile . && metacalc $workingfile
  mv ${workingfile%.*}.* $op/ && rm $op/$workingfile; cd $op;
fi


