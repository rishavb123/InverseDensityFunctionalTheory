#!/bin/bash
#SBATCH --mail-type=BEGIN,END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ARRAY_TASKS, ALL)
#SBATCH --job-name=CollectData
#SBATCH -A gts-amedford6
#SBATCH -N 1 --ntasks-per-node=1
#SBATCH --mem-per-cpu=7G
#SBATCH --mail-user=rbhagat8@gatech.edu  # Where to send mail
#SBATCH -t3:00:00
#SBATCH --output=CollectData_%A-%a.out           # Standard output and error log
#SBATCH -qinferno
cd $SLURM_SUBMIT_DIR
module load intel
module load anaconda3
module load mvapich2
source /storage/home/hcoda1/6/rbhagat8/sparc_env/bin/activate
source /storage/home/hcoda1/6/rbhagat8/data/sparc_env.sh
srun python /storage/home/hcoda1/6/rbhagat8/data/main.py