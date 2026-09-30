import os, sys
import argparse

template = """#!/bin/sh

#SBATCH --job-name={name}
#SBATCH --output={slurm_path}/output_logs/output_{name}.out
#SBATCH --error={slurm_path}/error_logs/error_{name}.err
#SBATCH --tasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=6GB
#SBATCH --time={time}
#SBATCH --account=lisa
#SBATCH --mail-user={user_mail}
#SBATCH --mail-type=ALL

source ~/.bashrc
module load conda
# module load gsl
# module load fftw
module load openmpi
conda activate lisabeta
source /pbs/home/a/amahdi/.conda/envs/lisabeta/lalsuite_for_lisabeta/etc/lalsuiterc


{executable} {script} {config}
"""

def activate_slurm_submit(config_name):

    subfile = '{}/submit_{}.sh'.format(sub_path, config_name.split('/')[-1].split('.ini')[0].split('config_')[-1])
    sys.stderr.write('generating {}\n'.format(subfile))

    with open(subfile,'w') as f:
        submission_command = template.format(name       = config_name.split('/')[-1].split('.ini')[0].split('config_')[-1],
                                             slurm_path = slurm_path,
                                             time       = '{}-{}:{}:00'.format(slurm_time['days'], slurm_time['hours'], slurm_time['minutes']),
                                             user_mail  = user_mail,
                                             executable = slurm_executable_path,
                                             script     = slurm_executable_file,
                                             config     = config_name)
                                             
        f.write(submission_command)
    sys.stderr.write('submitting {}\n\n'.format(subfile))
    os.system('sbatch "{}"'.format(subfile))

# ---------------------------------------------------------------------- #
parser = argparse.ArgumentParser(description="Generate slurm files")
parser.add_argument("config_dir", type=str, help="directory of input json files")
parser.add_argument("base_name", type=str, help="base_name of the run")
args = parser.parse_args()



user_mail    = 'asad.mahdi@l2it.in2p3.fr'
slurm_time   = {'days': 2, 'hours': 0, 'minutes': 0}
slurm_executable_path = 'MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 mpiexec -np 32 python'
slurm_executable_file = '/pbs/home/a/amahdi/lisabeta/src/lisabeta/inference/ptemcee_smbh.py'

# Set the specific directory for the runs
directory = f'/pbs/home/a/amahdi/PE for my work/{args.config_dir}/'
subdirectory = f'config_files/{args.base_name}'
# ---------------------------------------------------------------------- #

sub_path   = os.path.join(directory, f'submission_files/{args.base_name}')
slurm_path = os.path.join(directory, 'slurm_files')
if not os.path.exists(sub_path):
    os.makedirs(sub_path)

if not os.path.exists(slurm_path):
    os.makedirs(slurm_path)

if not os.path.exists(os.path.join(slurm_path, "output_logs")):
    os.makedirs(os.path.join(slurm_path, "output_logs"))

if not os.path.exists(os.path.join(slurm_path, "error_logs")):
    os.makedirs(os.path.join(slurm_path, "error_logs"))

if not (subdirectory == ''): final_path = os.path.join(directory, subdirectory)
else:                        final_path = directory
configs_path = os.path.join(os.getcwd(), final_path)
config_list  = os.listdir(configs_path)

print('')
for config in config_list:
    config_path = os.path.join(configs_path, config)
    activate_slurm_submit(config_path)

print('\nThe config files in {configs_path} are running in detached slurm jobs. Good luck!\n'.format(configs_path = configs_path))