from ase import *
from ase.io import read, write
import numpy as np

str1 = read('0.POSCAR')
str2 = read('1.POSCAR')
d1=[]
d2=[]
for i in np.r_[0:len(str1)]:
    for j in np.r_[i+1:len(str1)]:
        d1.append(str1.get_distance(i,j,mic=True))
        d2.append(str2.get_distance(i,j,mic=True))

diff = np.abs(np.sort(d1) - np.sort(d2))
print diff[np.argmax(diff)]
