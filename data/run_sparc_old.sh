#PBS -l nodes=8:ppn=1
#PBS -l walltime=3:00:00
#PBS -N molecule
#PBS -o stdout
#PBS -e stderr
#PBS -A GT-amedford6-joe
cd $PBS_O_WORKDIR
source ~/.bashrc
module load intel
cd $1
mpirun -np $PBS_NP /storage/home/hcoda1/6/rbhagat8/data/dev_SPARC/lib/sparc -name $2