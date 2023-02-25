import os
import time
import numpy as np
import itertools

from generate_input_files import write_input_files, make_atoms
from run_sparc import run_sparc


def run_pipeline(atoms_kwargs={}, directory=".", label="sparc-calc", user="rbhagat8"):
    os.makedirs(directory, exist_ok=True)
    atoms = make_atoms(**atoms_kwargs)
    write_input_files(label=label, atoms=atoms)
    proc_name = run_sparc(label=label, user=user)
    os.system(f"mv *.inpt *.ion *.pot *.out* *.static* *.csv* std* *.dens* {directory}")
    print(f"Finished process {proc_name}")


def build_str(positions):
    stamp = str(int(time.time()))[-5:]
    s = f"{stamp}_"
    for pos in positions:
        s += f"{pos[0]}-{pos[1]}-{pos[2]}_"
    return s[:-1]


def run_for_position(molecule_name="H2O", positions=None):
    path = (
        f"sparc_runs/{molecule_name}/{build_str(positions)}"
        if positions is not None
        else f"sparc_runs/{molecule_name}/default"
    )
    if os.path.isdir(path):
        os.rmdir(path)
    os.makedirs(path)
    run_pipeline(
        atoms_kwargs={"molecule_name": molecule_name, "positions": positions},
        directory=path,
    )


def main():
    dim_space = np.linspace(-1, 1, 3)
    pos_space = list(itertools.product(dim_space, dim_space, dim_space))
    positions_space = list(itertools.product(pos_space, pos_space, pos_space))

    for positions in positions_space:
        if tuple(positions[0]) == tuple(positions[1]) or tuple(positions[2]) == tuple(positions[1]) or tuple(positions[0]) == tuple(positions[2]):
            continue
        run_for_position(positions=positions)


if __name__ == "__main__":
    main()
