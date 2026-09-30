#!/bin/bash

#SBATCH --job-name=M1e6_SEOBv5_id_3_fti_dchi6lv_IMR
#SBATCH --output=/pbs/home/a/amahdi/PE_for_my_work/slurm_files/output_logs_id_4/output_M1e6_SEOBv5_id_3_fti_dchi6lv_IMR.out
#SBATCH --error=/pbs/home/a/amahdi/PE_for_my_work/slurm_files/error_logs_id_4/error_M1e6_SEOBv5_id_3_fti_dchi6lv_IMR.err
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

MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 mpiexec -np 24 --bind-to none python /pbs/home/a/amahdi/lisabeta/src/lisabeta/inference/ptemcee_smbh.py /pbs/home/a/amahdi/PE_for_my_work/./config_files/M1e6_SEOBv5_id_3/M1e6_SEOBv5_id_3_fti_dchi6lv_IMR.json
