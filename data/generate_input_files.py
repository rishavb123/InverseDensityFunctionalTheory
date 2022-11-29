from ase.build import molecule
from sparc.sparc_core import sparc

def make_sparc_calc():
    return SPARC(
        KPOINT_GRID=[1, 1, 1],
        h=0.2,
        EXCHANGE_CORRELATION='GGA_PBE',
        TOL_SCF=1e-6,
        # RELAX_FLAG=1,

        PRINT_FORCES=1,
        PRINT_ATOMS=1,
        PRINT_DENSITY=1,

        CALC_MCSH=1,
        MCSH_RADIAL_TYPE=1, # 1 or 2 : 1 is spherical harmonics --> set R_MAX and R_STEPSIZE (HSMP)
        MCSH_R_STEPSIZE=0.5,
        MCSH_MAX_ORDER=1, # max Spherical harmonic order
        MCSH_MAX_R=0.5, # max Rcut (size of the kernel); keep this to max of 2

        # raidal type 2 is (LPMP) basis is legendre polynomials times spherical harmonics
        # set the order of the polynomial (MCSH_MAX_ORDER=1)
        # if the radial order is 2,
        # 0, 1, 2 for 0 and 1 order

        directory='.',
        label='sparc-calc',
    )

def make_atoms(positions=None):
    atoms = molecule('H2O', positions=positions)
    atoms.set_cell([6, 6, 6])
    atoms.center()
    atoms.set_pbc([False] * 3)
    return atoms

def write_input_files(positions=None, directory='.', label='sparc-calc'):
    calc = make_sparc_calc()
    atoms = make_atoms(positions)
    atoms.set_calculator(calc)
    calc.write_input(directory=directory, label=label)

def main():
    write_input_files()

if __name__ == '__main__':
    main()
