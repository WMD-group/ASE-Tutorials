from ase.io import read, write

structure = read('958456.cif')
write('FormatePerovskite.POSCAR', structure, format='vasp', sort=True)
