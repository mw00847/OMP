#optimise a water acetone complex

import psi4
import numpy as np

#psi4 options
psi4.set_memory('4GB')
psi4.core.clean_options()

# Define basis and method
basis = '6-31G'
method = 'B3LYP'

complex=psi4.geometry("""
   
   O       -0.13754       -0.66135        1.57282
   C        0.04817        0.14202        0.67143
   C        1.37504        0.82389        0.53855
   C       -1.05047        0.44243       -0.30115
   H        1.82015        0.58464       -0.44982
   H        1.24015        1.92252        0.62208
   H        2.07166        0.48677        1.33563
   H       -1.96064       -0.14736       -0.06032
   H       -0.71949        0.18521       -1.32902
   H       -1.30209        1.52270       -0.25805
   --
   O        1.19823       -2.34435       -1.46339
   H        1.72061       -2.23825       -0.62887
   H        0.26309       -2.45726       -1.15789

""")

#optimise the complex
psi4.optimize(f'{method}/{basis}', molecule=complex)

#save the optimized geometry as a xyz file
complex.save_file('water_acetone_optimised.xyz')
print(complex)
