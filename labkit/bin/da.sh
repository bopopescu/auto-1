#!/bin/sh

dadir=$(basename `pwd`)

pspdir=psp
freqdir=freq
molecular_name=$1





if [ -d ../$pspdir ]; then
  cd ../$pspdir/
  mkdir NImag; ls ../$freqdir/NImag/|grep \.out|while read i;do mv $i NImag/;done
  ls *.out>list.txt
  findhf
  awk  '/.*out/{print $1"," $2} ' unique_list.txt |sed  '1i\Conformer,SP_Energy' |sed 's/.out//' >../$dadir/energy_list_$molecular_name.csv
else 
  echo 'no psp dir'
  exit 1
fi

if [ -d ../$freqdir ]; then
  cd ../$freqdir/
  mfreqchk $molecular_name
  cp *.csv ../$dadir/
else 
  echo 'no freq dir'
  exit 1
fi
cd ../$dadir
tempeture_distribution.R $molecular_name

cut -d',' -f2 Distributionc298K_$molecular_name.csv |head -10|tail -9 >most_distribution_$molecular_name.txt
j=0
cat most_distribution_$molecular_name.txt|while read i;do i=${i#\"};i=${i%\"};j=$((j+1));cp ../psp/$i.out ./$j.out;done
ls *.out >ofile
mout-xyz ofile
