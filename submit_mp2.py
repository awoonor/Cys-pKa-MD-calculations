import os
import paramiko
import sys
from pbs_generator import Pbs, Modules, ShellCommands, SshPbs

# Constants
NNODES_NVT = 1
NCPUS_NVT = 24
WALLTIME_NVT = '150h'
NNODES_NPT = 1
NCPUS_NPT = 24
WALLTIME_NPT = '150h'
orca_path = '/mnt/parallel_scratch_mp2_wipe_on_april_2017/rowley/ernesto/test/cysteine'
preparation_script = 'prep_mp2.sh'
queue = 'qwork'
# accounting_group = 'NAP_8961'

# SSH Instantiation
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect('rowley-mp2.ccs.usherbrooke.ca', username='ernesto', key_filename='/home/ernesto/.ssh/id_rsa.pub')
sftp = ssh.open_sftp()


def mkdir(dir):
    try:
        sftp.listdir(dir)
    except IOError:
        sftp.mkdir(dir)

# Upload PDB file
file = sys.argv[1]
name, extension = os.path.splitext(file)

local_pdb = os.path.realpath(file)
local_prep = os.path.realpath(preparation_script)
local_genion = os.path.realpath('assets/genion.mdp')
local_emin = os.path.realpath('assets/emin.mdp')
local_nvt = os.path.realpath('assets/nvt_long.mdp')
local_npt = os.path.realpath('assets/npt_long.mdp')

local_mklambdas = os.path.realpath('assets/mklambdas_long.py')
local_fep_long = os.path.realpath('assets/fep_long.mdp')
local_topol_other = os.path.realpath('assets/topol_Other_chain_I_fep.itp')

remote_main_dir = os.path.join(orca_path, name)
mkdir(remote_main_dir)

sftp.put(local_prep, os.path.join(remote_main_dir, 'prep.sh'))
sftp.put(local_pdb, os.path.join(remote_main_dir, file))
sftp.put(local_genion, os.path.join(remote_main_dir, 'genion.mdp'))
ssh.exec_command('sh %s/prep.sh %s %s >> %s/prep.log' % (remote_main_dir, remote_main_dir, name, remote_main_dir))

modules = Modules().purge().load('intel64/15.3.187 openmpi/2.0.1_intel15 gromacs/5.1.4')

# Energy Minimization
remote_em_dir = os.path.join(remote_main_dir, '1_em')
print 'Making a directory: %s' % remote_em_dir
mkdir(remote_em_dir)
sftp.put(local_emin, os.path.join(remote_em_dir, 'run.mdp'))

commands = ShellCommands() \
    .cd(remote_em_dir) \
    .gmx_mpi('grompp -f run.mdp -c ../%s_solv-ions.gro -p ../topol.top -o topol.tpr' % name) \
    .gmx_mpi('mdrun')

em = SshPbs(modules, commands, ssh=ssh) \
    .name('%s_EM' % name) \
    .open_mp(1) \
    .wall_time('1h') \
    .queue(queue) \
    .submit()

# NVT
remote_nvt_dir = os.path.join(remote_main_dir, '2_nvt')
print 'Making a directory: %s' % remote_nvt_dir
mkdir(remote_nvt_dir)
sftp.put(local_nvt, os.path.join(remote_nvt_dir, 'run.mdp'))

commands = ShellCommands() \
    .append('#PBS -l nodes=%d' % NNODES_NVT) \
    .cd(remote_nvt_dir) \
    .gmx_mpi('grompp -f run.mdp -c ../1_em/confout.gro -p ../topol.top -o topol.tpr') \
    .mpirun('-np %d /cvmfs/opt.usherbrooke.ca/gromacs/5.1.4/bin/gmx_mpi mdrun -s topol.tpr' % (NCPUS_NVT))

nvt = SshPbs(modules, commands, ssh=ssh) \
    .name('%s_NVT' % name) \
    .wall_time(WALLTIME_NVT) \
    .queue(queue) \
    .depends(em) \
    .submit()

# NPT
remote_npt_dir = os.path.join(remote_main_dir, '3_npt')
print 'Making a directory: %s' % remote_npt_dir
mkdir(remote_npt_dir)
sftp.put(local_npt, os.path.join(remote_npt_dir, 'run.mdp'))

commands = ShellCommands() \
    .append('#PBS -l nodes=%d' % NNODES_NPT) \
    .cd(remote_npt_dir) \
    .gmx_mpi('grompp -f run.mdp -c ../2_nvt/confout.gro -t ../2_nvt/state.cpt -p ../topol.top -o topol.tpr') \
    .mpirun('-np %d /cvmfs/opt.usherbrooke.ca/gromacs/5.1.4/bin/gmx_mpi mdrun -s topol.tpr' % (NCPUS_NPT))

npt = SshPbs(modules, commands, ssh=ssh) \
    .name('%s_NPT' % name) \
    .wall_time(WALLTIME_NPT) \
    .queue(queue) \
    .depends(nvt) \
    .submit()

# Replica
remote_replica_dir = os.path.join(remote_main_dir, '4_replica')
mkdir(remote_replica_dir)
print 'Making a directory: %s' % remote_replica_dir
sftp.put(local_mklambdas, os.path.join(remote_replica_dir, 'mklambdas_long.py'))
sftp.put(local_fep_long, os.path.join(remote_replica_dir, 'fep_long.mdp'))
sftp.put(local_topol_other, os.path.join(remote_replica_dir, 'topol_Other_chain_I_fep.itp'))

# print em
# print nvt
# print npt

ssh.close()
