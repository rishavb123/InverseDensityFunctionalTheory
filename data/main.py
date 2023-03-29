import os
import time
import numpy as np
import itertools

from generate_input_files import write_input_files, make_atoms
from run_sparc import run_sparc


def run_pipeline(atoms_kwargs={}, directory=".", label="sparc-calc", user="rbhagat8"):
    """Runs the full pipeline from generating inputs files and running sparc and generating output files

    Args:
        atoms_kwargs (dict, optional): The arguments to send to make_atoms. Defaults to {}.
        directory (str, optional): The directory to save the input files and run sparc in. Defaults to ".".
        label (str, optional): The label to run sparc with. Defaults to "sparc-calc".
        user (str, optional): The user to run sparc with. Defaults to "rbhagat8".
    """
    os.makedirs(directory, exist_ok=True)
    atoms = make_atoms(**atoms_kwargs)
    write_input_files(label=label, atoms=atoms)
    proc_name = run_sparc(label=label, user=user)
    os.system(f"mv *.inpt *.ion *.pot *.out* *.static* *.csv* std* *.dens* {directory}")
    print(f"Finished process {proc_name}")


def build_str(positions):
    """Builds the directory string using atomic positions

    Args:
        positions (list): The list of three positions (x, y, and z coordinates)

    Returns:
        str: The built string for the directory
    """
    stamp = str(int(time.time()))[-5:]
    s = f"{stamp}_"
    for pos in positions:
        s += f"{pos[0]}-{pos[1]}-{pos[2]}_"
    return s[:-1]


def run_for_position(molecule_name="H2O", positions=None):
    """Runs the pipeline given a molecule name and the atomic positions

    Args:
        molecule_name (str, optional): The molecule name. Defaults to "H2O".
        positions (list, optional): The atomic positions. Defaults to None.
    """
    parent_dir = "/storage/home/hcoda1/6/rbhagat8/p-amedford6-0"
    path = (
        f"{parent_dir}/sparc_runs/{molecule_name}/{build_str(positions)}"
        if positions is not None
        else f"{parent_dir}/sparc_runs/{molecule_name}/default"
    )
    if os.path.isdir(path):
        os.rmdir(path)
    os.makedirs(path)
    run_pipeline(
        atoms_kwargs={"molecule_name": molecule_name, "positions": positions},
        directory=path,
    )


def main():
    """Runs the sparc pipeline a bunch for many different data points"""
    N = 100000

    for i in range(N):
        positions = [np.random.random(3) * 2 - 1 for _ in range(3)]

        if (
            tuple(positions[0]) == tuple(positions[1])
            or tuple(positions[2]) == tuple(positions[1])
            or tuple(positions[0]) == tuple(positions[2])
        ):
            continue
        run_for_position(positions=positions)
        print(f"generated {i + 1}/{N} configurations")


if __name__ == "__main__":
    main()
