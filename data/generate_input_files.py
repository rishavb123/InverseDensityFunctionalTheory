import os

from ase.build import molecule
from sparc.sparc_core import SPARC

def make_sparc_calc(directory=".", label="sparc-calc"):
    """Builds the sparc calc object

    Args:
        directory (str, optional): The directory to run sparc in. Defaults to ".".
        label (str, optional): The label to run sparc with. Defaults to "sparc-calc".

    Returns:
        SPARC: A sparc calculator object
    """
    return SPARC(
        KPOINT_GRID=[1, 1, 1],
        h=0.2,
        EXCHANGE_CORRELATION="GGA_PBE",
        TOL_SCF=1e-6,
        # RELAX_FLAG=1,
        PRINT_FORCES=1,
        PRINT_ATOMS=1,
        PRINT_DENSITY=1,
        CALC_MCSH=1,
        MCSH_RADIAL_TYPE=1,  # 1 or 2 : 1 is spherical harmonics --> set R_MAX and R_STEPSIZE (HSMP)
        MCSH_R_STEPSIZE=0.5,
        MCSH_MAX_ORDER=1,  # max Spherical harmonic order
        MCSH_MAX_R=0.5,  # max Rcut (size of the kernel); keep this to max of 2
        # raidal type 2 is (LPMP) basis is legendre polynomials times spherical harmonics
        # set the order of the polynomial (MCSH_MAX_ORDER=1)
        # if the radial order is 2,
        # 0, 1, 2 for 0 and 1 order
        directory=directory,
        label=label,
    )


def make_atoms(
    molecule_name="H2O", positions=None, cell=[6, 6, 6], pbc=[False, False, False]
):
    """Creates the molecule object

    Args:
        molecule_name (str, optional): The molecule name. Defaults to "H2O".
        positions (list, optional): The list of atomic positions. Defaults to None.
        cell (list, optional): The cell to contain the molecule in. Defaults to [6, 6, 6].
        pbc (list, optional): The pbc. Defaults to [False, False, False].

    Returns:
        molecule: The molecule object
    """
    atoms = molecule(molecule_name, positions=positions)
    atoms.set_cell(cell)
    atoms.center()
    atoms.set_pbc(pbc)
    return atoms


def write_input_files(directory=".", label="sparc-calc", atoms=None):
    """Writes the input files for a specified sparc run

    Args:
        directory (str, optional): The directory to write to. Defaults to ".".
        label (str, optional): The label to run sparc with. Defaults to "sparc-calc".
        atoms (molecule, optional): The molecule object. Defaults to None.
    """
    calc = make_sparc_calc(directory, label)
    atoms = atoms if atoms is not None else make_atoms()
    atoms.set_calculator(calc)
    calc.write_input()
    if directory is not '.':
        os.system(f'mv *.inpt *.ion *.pot {directory}')

if __name__ == "__main__":
    write_input_files()