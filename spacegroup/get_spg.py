#!/usr/bin/env python

import ase.io.vasp as io
from pyspglib import spglib
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",
                  action="store", type="string", dest="file", default="POSCAR",
                  help="Path to input file [default: ./POSCAR]")
parser.add_option("-p", "--prec",
                  action="store", type="float", dest="prec", default=0.001,
                  help="Precision for symmetry test [default: 0.001]")
(options, args) = parser.parse_args()

bulk = io.read_vasp(options.file)
spacegroup = spglib.get_spacegroup(bulk, symprec=options.prec)

print "Spacegroup information."
print "-----------------------"
print spacegroup
print "-----------------------"
