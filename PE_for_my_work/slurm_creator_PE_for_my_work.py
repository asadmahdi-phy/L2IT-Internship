import os, sys
import argparse
import shlex

template = """#!/bin/bash

#SBATCH --job-name={name}
#SBATCH --output=/pbs/home/a/amahdi/PE_for_my_work/slurm_files/output_logs_id_2/output_{name}.out
#SBATCH --error=/pbs/home/a/amahdi/PE_for_my_work/slurm_files/error_logs_id_2/error_{name}.err
#SBATCH --tasks-per-node=24
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=6GB
#SBATCH --time=2-00:00:00
#SBATCH --account=lisaf
#SBATCH --licenses=sps
#SBATCH --mail-user=asad.mahdi@l2it.in2p3.fr
#SBATCH --mail-type=ALL

#source ~/.bashrc
module load conda
#module load gsl
#module load fftw
module load openmpi
conda activate lisabeta
#unset PYTHONPATH
#export PYTHONNOUSERSITE=1
source /pbs/home/a/amahdi/.conda/envs/lisabeta/lalsuite_for_lisabeta/etc/lalsuiterc

{executable} {script} {config}
"""

def activate_slurm_submit(config_name):

    run_name = config_name.split('/')[-1].split('.json')[0].split('config_')[-1]
    subfile = '{}/submit_{}.sh'.format(sub_path, run_name)
    sys.stderr.write('generating {}\n'.format(subfile))

    with open(subfile,'w') as f:
        submission_command = template.format(name       = run_name,
                                             slurm_path = slurm_path,
                                             time       = '{}-{}:{}:00'.format(slurm_time['days'], slurm_time['hours'], slurm_time['minutes']),
                                             user_mail  = user_mail,
                                             executable = slurm_executable_path,
                                             script     = shlex.quote(slurm_executable_file),
                                             config     = shlex.quote(config_name))

        f.write(submission_command)
    sys.stderr.write('submitting {}\n\n'.format(subfile))
    os.system('cd {} && sbatch {}'.format(shlex.quote(directory), shlex.quote(subfile)))

# ---------------------------------------------------------------------- #
parser = argparse.ArgumentParser(description="Generate slurm files")
parser.add_argument("config_dir", type=str, help="directory of input json files")
parser.add_argument("base_name", type=str, help="base_name of the run")
args = parser.parse_args()



user_mail = 'asad.mahdi@l2it.in2p3.fr'

slurm_time = {'days': 2, 'hours': 0, 'minutes': 0}

slurm_executable_path = (
    'MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 '
    'NUMEXPR_NUM_THREADS=1 '
    'mpiexec -np 24 --bind-to none python'
)

slurm_executable_file = '/pbs/home/a/amahdi/lisabeta/src/lisabeta/inference/ptemcee_smbh.py'

# Set the specific directory for the runs
directory = f'/pbs/home/a/amahdi/PE_for_my_work/{args.config_dir}/'
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

if not os.path.exists(configs_path):
    print('')
    print('ERROR: Config folder not found:')
    print(configs_path)
    print('')
    print('You need to run the JSON config creator first. For example:')
    print('python json_config_creator_SEOBNRv5HMROM_params_PE_for_my_work_fixed.py ./ M1e6 IMR 1e6 333021.2829607493 0 0.2 1 0.35 SEOBv5')
    print('')
    print('Then submit with:')
    print('python slurm_creator_PE_for_my_work.py . M1e6_SEOBv5')
    sys.exit(1)

config_list  = [f for f in os.listdir(configs_path) if f.endswith('.json')]

if len(config_list) == 0:
    print('')
    print('ERROR: No .json config files found in:')
    print(configs_path)
    print('')
    print('Please check that the JSON config creator generated the config files correctly.')
    sys.exit(1)

print('')
for config in config_list:
    config_path = os.path.join(configs_path, config)
    activate_slurm_submit(config_path)

print('\nThe config files in {configs_path} are running in detached slurm jobs. Good luck!\n'.format(configs_path = configs_path))