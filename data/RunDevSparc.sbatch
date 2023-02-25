#!/bin/bash
#SBATCH --mail-type=BEGIN,END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ARRAY_TASKS, ALL)
#SBATCH --job-name=RunDevSparc
#SBATCH -A gts-amedford6
#SBATCH -N 2 --ntasks-per-node=4
#SBATCH --mem-per-cpu=7G
#SBATCH --mail-user=rbhagat8@gatech.edu  # Where to send mail
#SBATCH -t3:00:00
#SBATCH --output=RunDevSparc_%A-%a.out           # Standard output and error log
#SBATCH -qinferno
cd $SLURM_SUBMIT_DIR
module load intel
module load mvapich2
cd $directory
srun /storage/home/hcoda1/6/rbhagat8/data/dev_SPARC/lib/sparc -name $label