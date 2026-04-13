#!/bin/sh

module purge
module load intel64/15.3.187 openmpi/2.0.1_intel15 gromacs/5.1.4

cd $1

gmx_mpi pdb2gmx -ignh -f $2.pdb -water tip3p -ff charmm36-nov2016
gmx_mpi editconf -f conf.gro -o $2_box.gro -c -d 1.0 -bt cubic
gmx_mpi solvate -cp $2_box.gro -cs spc216.gro -p topol.top -o $2_solv.gro
gmx_mpi grompp -f genion.mdp -c $2_solv.gro -p topol.top -o ions.tpr
echo "13" | gmx_mpi genion -s ions.tpr -o $2_solv-ions.gro -p topol.top -pname NA -pq 1 -nname CL -nq -1 -conc 0.1 -neutral
