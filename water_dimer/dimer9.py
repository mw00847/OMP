import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# above is needed to avoid the below error
# OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
# OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.

import autode as ade
import numpy as np
import matplotlib.pyplot as plt
import psi4
import glob

# 'optimised' water dimer
dimer = ade.Molecule(atoms=[

    ade.Atom("O", 0.00000000, 0.00000000, 1.64724900),
    ade.Atom("O", 0.00000000, 0.00000000, -1.41033300),
    ade.Atom("H", 0.00000000, 0.75046200, 1.04528700),
    ade.Atom("H", 0.00000000, -0.75046200, 1.04528700),
    ade.Atom("H", 0.76503500, 0.00000000, -1.99295300),
    ade.Atom("H", -0.76503500, 0.00000000, -1.99295300)
])

# Indices of atoms to be translated
idxs = (1, 4, 5)  # NOTE: atoms are 0 indexed

# Calculate the unit vector from O1 to O2 (index 0 to 3)
vec = dimer.atoms.nvector(0, 1)
unit_vec = vec / np.linalg.norm(vec)

# Initial distance
r0 = dimer.atoms.distance(0, 1)

# range of distances
r_values = np.arange(1, 5, 0.2)


# Function to update coordinates
def update_coordinates(dimer, r, idxs, unit_vec, r0):
    new_dimer = dimer.copy()  # Create a copy to avoid modifying the original dimer
    for i in idxs:
        atom = new_dimer.atoms[i]
        atom.coord += unit_vec * (r - r0)
    return new_dimer


# loop through increasing distances between
for r in r_values:
    translated_dimer = update_coordinates(dimer, r, idxs, unit_vec, r0)
    filename = f"dimer9_translated_{r:.1f}.xyz"
    translated_dimer.print_xyz_file(filename=filename)

# Clear psi4 output
psi4.core.clean()


def read_xyz(filename):
    with open(filename, 'r') as file:
        contents = file.read()
    return contents


import glob

# create a list of the XYZ files
xyz_files = glob.glob("dimer9_translated_*.xyz")
print(xyz_files)


def run_psi4(xyz_files):
    def read_xyz(filename):
        with open(filename, 'r') as file:
            contents = file.read()
        return contents

    # Set up Psi4 use b3lyp and 6-31G
    psi4.set_options({'basis': '6-31G**', 'reference': 'rhf'})
    psi4.set_memory('4 GB')

    # Loop through the XYZ files and calculate energy
    energies = []
    for xyz_file in xyz_files:
        # Read the XYZ file contents
        xyz_contents = read_xyz(xyz_file)

        # Create Psi4 molecule from XYZ contents
        molecule = psi4.geometry(xyz_contents)

        # Calculate the energy
        energy = psi4.energy('scf/sto-3g', molecule=molecule)
        energies.append((float(xyz_file.split('_')[-1].split('.xyz')[0]), energy))
        print(f"Energy for {xyz_file}: {energy} Hartree")

    # Sort energies based on r values
    energies.sort(key=lambda x: x[0])

    # Unpack r_values and energies for plotting
    r_values, energy_values = zip(*energies)

    # Plot the energy profile
    plt.plot(r_values, energy_values, 'o-')
    plt.xlabel('Distance (Å)')
    plt.ylabel('Energy (Hartree)')
    plt.title('Energy Profile of Water Dimer Translation')
    plt.show()

    #save the data as a numpy array
    np.save('energy_values_dimer9.npy', energy_values)
    np.save('r_values_dimer9.npy', r_values)


# Call the run_psi4 function
run_psi4(xyz_files)
