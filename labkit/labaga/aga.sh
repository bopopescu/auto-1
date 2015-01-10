#!/bin/sh
#modify the following three links
TOOLS=/home/lvxb/code/aga/tools/
GA=/home/lvxb/code/aga/src/
POTFIT=/home/lvxb/bin/potfit.eam.anl

runlog=log.aga        #log file name
tmp=`sed -n 21p ga.in`
set -- $tmp
nconfig=$(($1))   #number of configurations selected for potfit (in the order of E).
                  #optional; default is to use all the dft calculated configurations.
if [ ! -d "tmpdata" ]; then
  mkdir tmpdata/
fi
NCPU=`wc -l < nodes`

i=1
echo "###  SEARCH STARTS  ###" > $runlog
tmp=`sed -n 6p ga.in`
set -- $tmp
Niteration=$(($2))
while [ $i -le $Niteration ]
do
  echo "running iteration #$i ..." >> $runlog
  #----ga----#
  mpirun -machinefile nodes -np $NCPU $GA/ga.x > ga.out_$i
  echo -e "\t GA done." >> $runlog

  #----vasp----#
  #vasp station: read from ga.in
  tmp=`sed -n 4p ga.in`
  set -- $tmp
  vstation=$(($2))
  vcpu=$((NCPU / vstation))

  echo -e "\t $vstation stations for vasp calculation." >> $runlog
  echo -e "\t $vcpu CPUs for each vasp job." >> $runlog

  total=`ls -l POSCAR_* | wc -l`
  if [ $total -lt $vstation ]; then
    echo "#Warning: station number is larger than structures to be calculated." >> $runlog
    vstation=$((total))
  fi

  j=1
  while [ $j -le $vstation ]
  do
    if [ -d "runvasp$j" ]; then
      rm -r runvasp$j/*
    else
      mkdir runvasp$j/
    fi
    aline=$((j*vcpu-vcpu+1))
    bline=$((aline+vcpu-1))
    sed -n $aline,$bline\p nodes > runvasp$j/sub_nodes

    mv POSCAR_$j runvasp$j/POSCAR
    cp vaspfiles/* runvasp$j/
    cd runvasp$j/
    ./run-vasp.sh $total $j $runlog &
    cd ..
    let j++
  done
  wait

  #----potfit----#
  tmp=`sed -n 10p ga.in`
  set -- $tmp
  ntype=$(($1 - 1))
  echo -e "\t doing potfit ..." >> $runlog
  vasp2force -e atom_energy.dat tmpdata/OUTCAR_* > config
  nstr=`grep E config | wc -l`
  echo -e "\t $nstr configurations found." >> $runlog
  if [ $nconfig -eq 0 ]; then
    nconfig=$(($nstr))
  fi
  echo -e "\t $nconfig configurations are used for potfit." >> $runlog
  $TOOLS/selectconfig.x config $ntype $nstr $nconfig
  $POTFIT potfit.in > potout_$i

  #---save data----#
  echo -e "\t storing data ..." >> $runlog
  $TOOLS/config2pool.x config $ntype $nstr dft_pool_$i     #dft pool from config file
#  cp tmpdata/POSCAR_* .
#  $TOOLS/poscar2pool.x $ntype $nstr dft_pool_$i    #dft pool from POSCAR files
  mv config          config_$i
  mv pot.config      pot.config_$i
  mv results.pool    classical_pool_$i
  cp pot.lammps      potential_$i 
  cp mypot_start     my_apot_$i
  cp new_pot.alloy   pot.lammps
#  cp out.lammps.EAM  pot.lammps
  cp mypot_end       mypot_start

  echo -e "iteration #$i finished." >> $runlog
  echo "#---------------------#" >> $runlog
  #---clean data---#
  rm tmpdata/* eands.dat out.* *.tmp results.pool0 

  let i++
done
