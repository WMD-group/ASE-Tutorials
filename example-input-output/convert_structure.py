# Useage python convert_structure.py -f <input> -o <output>
from ase.io import read, write
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",
                  action="store", type="string", dest="file", default="Entry.cif",
                  help="Path to input file [default: ./Entry.cif]")
parser.add_option("-o", "--out",
                  action="store", type="string", dest="output", default="POSCAR.out",
                  help="Output file [default: POSCAR.out]")
# Add further options here
(options, args) = parser.parse_args()
# Ensire that the input files exist

structure = read(options.file)
write(options.output, structure, format='vasp', sort=True)
