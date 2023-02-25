# loading the modules

module purge
module load intel
module load anaconda3
module load mvapich2

export PATH=/storage/home/hcoda1/6/rbhagat8/data/dev_SPARC/lib:$PATH
export PYTHONPATH=/storage/home/hcoda1/6/rbhagat8/data/ase:$PYTHONPATH
export PATH=/storage/home/hcoda1/6/rbhagat8/data/ase/bin:$PATH
export PYTHONPATH=/storage/home/hcoda1/6/rbhagat8/data/sparc-dft-api/:$PYTHONPATH
export SPARC_PSP_PATH=/storage/home/hcoda1/6/rbhagat8/data/sparc-dft-api/sparc/pseudos/PBE_pseudos

if [[ -z "${PBS_NP}" ]]; then
  export ASE_SPARC_COMMAND="/home/hcoda1/6/rbhagat8/data/dev_SPARC/lib/sparc -name PREFIX"
else
  export ASE_SPARC_COMMAND="mpirun -np $PBS_NP /home/hcoda1/6/rbhagat8/data/dev_SPARC/lib/sparc -name PREFIX"
fi