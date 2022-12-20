import os
import time

from generate_input_files import write_input_files, make_atoms
from run_sparc import run_sparc


def run_pipeline(atoms_kwargs={}, directory='.', label='sparc-calc', user='rbhagat8'):
    os.makedirs(directory, exist_ok=True)
    atoms = make_atoms(**atoms_kwargs)
    write_input_files(label=label, atoms=atoms)
    proc_name = run_sparc(label=label, user=user)
    os.system(f'mv *.inpt *.ion *.pot *.out* *.static* *.csv* std* *.dens* {directory}')
    print(f"Finished process {proc_name}")

def main():
    stamp = int(time.time())
    run_pipeline(directory=f'temp_results/{stamp}')

if __name__ == "__main__":
    main()