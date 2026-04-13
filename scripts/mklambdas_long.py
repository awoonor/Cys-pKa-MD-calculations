#!/usr/bin/env python

import os, sys, shutil

lambdas=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

fh=open('fep_long.mdp', 'r')
lines=fh.readlines()
fh.close()

all_lam=""
for l in lambdas:
    all_lam=all_lam + str(l) + ', '
all_lam=all_lam[:-2]

state=0
for lam in lambdas:
    ldir='lambda_' + ('%02d' % state)
    print ldir
    os.mkdir(ldir)
    os.system('cp *.itp ' + ldir)
    shutil.copyfile(sys.argv[1], ldir + '/topol.top')
    fh=open(ldir + '/grompp.mdp', 'w')
    for l in lines:
        newline=str.replace(l,'$STATE$', str(state))
        newline=str.replace(newline, '$ALL_LAMBDAS$', str(all_lam))
	newline=str.replace(newline, '$GEN_VEL$', "no")
	if(newline.startswith("gen-temp")):
		newline=";"+newline
	if(newline.startswith("gen-seed")):
		newline=";"+newline+"continuation		 =yes\n"
        fh.write(newline)
    fh.close()
    os.chdir(ldir)
    os.system('gmx grompp -f grompp.mdp  -c ../3_npt/confout.gro -t ../3_npt/state.cpt -p topol.top -o topol.tpr -maxwarn 2 -zero >& grompp.log')
    os.chdir('..')
    state=state+1
