import psi4

def init():
    psi4.core.set_output_file('output.dat', False)
    psi4.set_memory('500 MB')

def create_molecule():
    h2o = psi4.geometry("""
        O
        H 1 0.96
        H 1 0.96 2 104.5
    """)

    return h2o

def calculate_energy():

    energy = psi4.energy('scf/cc-pvdz')

    return energy

def main():

    init()

    h2o = create_molecule()
    energy = calculate_energy()

    print(energy)

if __name__ == '__main__':
    main()