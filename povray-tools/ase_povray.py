#!/usr/bin/env python
from ase.data import colors
import numpy as np
class povray_parameter:
    def __init__(self,atoms,atoms_radii=''):
	self.atoms=atoms
        self.kwargs = {
	    'rotation'      : '', # text string with rotation (default='' )
	    'radii'         : .85, # float, or a list with one float per atom
	    'colors'        : None,# List: one (r, g, b, t) tuple per atom
	    'show_unit_cell': 0,   # 0, 1, or 2 to not show, show, and show all of cell
	    }
	
# Extra kwargs only avaliable for povray (All units in angstrom)
    	self.kwargs.update({
	    'run_povray'   : True, # Run povray or just write .pov + .ini files
	    'display'      : False,# Display while rendering
	    'pause'        : True, # Pause when done rendering (only if display)
	    'transparent'  : True,# Transparent background
	    'canvas_width' : 500, # Width of canvas in pixels
	    'canvas_height': None, # Height of canvas in pixels
	    'camera_dist'  : 50.,  # Distance from camera to front atom
	    'image_plane'  : None, # Distance from front atom to image plane
	    'camera_type'  : 'orthographic', # perspective, ultra_wide_angle
	    'point_lights' : [], #[(18,20,40), 'White'],[(60,20,40),'White'],             # [[loc1, color1], [loc2, color2],...]
	    'area_light'   : [(2., 3., 125.), # location
	                      'White',       # color
	                      .95, .8, 5, 4], # width, height, Nlamps_x, Nlamps_y
	    'background'   : 'White',        # color
	    'textures'     : None, # Length of atoms list of texture names
	    'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
            'bondlinewidth'  : 0.10, # Radius of the cylinders representing the bonds
            'bondatoms'      : [],   # [[atom1, atom2], ... ] pairs of bonding atoms
            'bbox'	   : None,
})
	farver=[]
	text=[]
        for a in self.atoms:
	    farver.append(colors.jmol_colors[a.get_atomic_number(),:])
            text.append('ase3')
	self.kwargs['colors']=farver
        self.kwargs['textures']=text

	if atoms_radii!='':
	    self.set_radii(atoms_radii)

    def set_radii(self,atoms_radii):
        syms=self.atoms.get_chemical_symbols()
	radii=[]	
	for s in syms:
	    radii.append(atoms_radii[s])
	self.kwargs['radii']=radii

    def set_colors(self,atoms_colors):
	syms=self.atoms.get_chemical_symbols()
	farver=[]
	for s in syms:
	    farver.append(np.array(atoms_colors[s]))
	self.kwargs['colors']=farver

    def set_textures(self,atoms_textures):
	syms=self.atoms.get_chemical_symbols()
	text=[]	
	for s in syms:
	    text.append(atoms_textures[s])
	self.kwargs['textures']=text

    def set_specific_radii(self,at,at_rad):
        radii=self.kwargs['radii']
	for i in range(len(at)):
	    radii[at[i]]=at_rad[i]
	self.kwargs['radii']=radii

    def set_specific_textures(self,at,at_text):
        text=self.kwargs['textures']
	for i in range(len(at)):
	    text[at[i]]=at_text[i]
	self.kwargs['textures']=text


    def set_specific_colors(self,at,at_color):
	farver=self.kwargs['colors']
	for i in range(len(at)):	
	    if type(at_color[i])==float or type(at_color[i])==int:
		farve=farver[at[i]]*at_color[i]
		farver[at[i]]=np.array([min(1,farve[0]),min(1,farve[1]),min(1,farve[2])])

	    else:
	        farver[at[i]]=at_color[i]
	self.kwargs['colors']=farver

	



    
