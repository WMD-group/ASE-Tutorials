from ase.lattice import bulk
from ase.dft.kpoints import *
import numpy as np
import os
import ase
from ase.calculators.vasp import Vasp
from ase.lattice.spacegroup import crystal
import matplotlib.pyplot as plt

def primitive_from_conventional_cell(atoms, spacegroup=1, setting=1):
    """Returns primitive cell given an Atoms object for a conventional
    cell and it's spacegroup."""
    from ase.lattice.spacegroup import Spacegroup
    from ase.utils.geometry  import cut
    sg = Spacegroup(spacegroup, setting)
    prim_cell = sg.scaled_primitive_cell  # Check if we need to transpose
    return cut(atoms, a=prim_cell[0], b=prim_cell[1], c=prim_cell[2])

#Define the coordinates
bulk = ase.io.read('GaN.cif')
zns = primitive_from_conventional_cell(bulk)

# Define KPOINTS for special points
points = ibz_points['hexagonal']
G = points['Gamma']
A = points['A']
M = points['M']
H = points['H']
L = points['L']
kpoints, x, X = get_bandpath([A,L,M,G,A,H], zns.cell, npoints=60)
# Point names for plot axis
point_names = ['A','L','M','G','A','H']

# FROM HERE ON NO REAL INPUT IS NEEDED, UNLESS ONE WISHES TO
# CHANGE SOME VASP INCAR PARAMETERS

# Define the first calculation
calc_single = Vasp(system = "Generic System Name",
               istart = 0,iniwav = 1,icharg = 0,gamma=True,reciprocal=True,
               prec="Accurate", lreal = False, algo = "Normal", encut = 500.00,
               nelm = 200, ediff = 1e-6, gga = "PS",kpts=(4,4,4),
               ediffg = 1e-3, nsw = 0, ibrion = 1, isif = 3, isym = 2,
               ismear = -5)

zns.set_calculator(calc_single)
energy = zns.get_potential_energy()
print("Energy: ",energy)
print("Moving to band structure calculation")

# Get the kpoints from run 1 and make the VASP kpoint file for run 2
ibzkpts = calc_single.get_ibz_k_points()
weights = calc_single.read_k_point_weights()
kpts = np.concatenate((ibzkpts,kpoints))
dummy = np.zeros(shape=(len(kpts),4))
for i in range(len(ibzkpts)):
    dummy[i,3] = weights[i]

dummy[:,:-1] = kpts
kpts = dummy 

# Define the band structure calculation
calc_band = Vasp(system = "Band structure",
               encut = 500.00,
               gga = "PS",
	       kpts=kpts,
               nsw = 0,
               ismear = 0, 
	       sigma = 0.01,
	       reciprocal = True)
zns.set_calculator(calc_band)
print "Band Calc"
bands = zns.get_potential_energy()

# Get the band energies across the Brillouin zone
e_kn = np.array([calc_band.get_eigenvalues(k) for k in range(len(kpts))])
# Get Fermi energy
ef = calc_band.get_fermi_level()
nbands = calc_band.get_number_of_bands()

# Plotting time
e_kn -= ef
emin = e_kn.min() - 1.0
emax = e_kn[:, nbands-1].max() + 1.0

# Plot the energy Vs k-point for each band
nelect = calc_band.get_number_of_electrons()
for n in range(nbands):
# Choose colour based on valence or conduction
    for n in range(nbands):
	if n < nelect/2:
	    plt.plot(x, e_kn[len(ibzkpts):len(kpts), n],color='#800000')
	else:
	    plt.plot(x, e_kn[len(ibzkpts):len(kpts), n],color='#228B22')

# Shade in valence and conduction bands
plt.fill_between(x,emin,e_kn[len(ibzkpts):len(kpts), nelect/2 - 1],color='#800000',alpha=0.6)
plt.fill_between(x,e_kn[len(ibzkpts):len(kpts), nelect/2],emax,color='#228B22',alpha=0.6)

# Set thick lines at each k-point
for p in X:
    plt.plot([p, p], [emin, emax], 'k-')

# Set the axis tick marks and labels
plt.plot([0, X[-1]], [0, 0], 'k-')
plt.xticks(X, ['$%s$' % n for n in ['A', 'L','M', r'\Gamma', 'A', 'H']])
plt.axis(xmin=0, xmax=X[-1], ymin=emin, ymax=emax)
plt.xlabel('k-vector')
plt.ylabel('E-$E_F$ (eV)')

# Save the plot
plt.savefig('bands.pdf')



