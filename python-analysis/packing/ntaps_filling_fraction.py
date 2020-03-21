#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:30:35 2020

@author: Noah
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scp
import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter

variable = "ntaps_corrected"
#gamma = 0.01
gammas = [0.01, 0.02, 0.03, 0.06]

filestem = str("/Users/Noah/remote/LIGGGHTS/Run/ContactModel/" + 
               "packing/forced_packing/filling_tapping/setup/test/continuous_measure_8000/")

filelist = []
for i in range(0, len(gammas)):
    filelist.append(filestem + "gamma" + str(gammas[i])+"/")

# Cavity pocket dimensions
R = 3e-3    #radius of pocket
h = 1.5e-3  #height of pocket
V_reg = np.pi*(R**2)*h  #volume of pocket

# Average Particle Dimensions
r1 = 100e-6 #radius of particle (average)
v_p = (4/3)*np.pi*(r1**3)   #volume of particle (average)
p_c = (v_p/V_reg)   #percent filled by one particle

# Figure setup
fig1 = plt.figure(1)
plt.xlabel("Number of taps")
plt.ylabel("Cavity Packing Fraction")
plt.title("Packing Fraction with Tapping")

for fname in filelist:
    data = np.loadtxt(fname+ "post/no_particles.txt", skiprows = 2)
    a = filelist.index(fname)
    b = data[:,2]*p_c
    c = []
    d = []
    for i in range(0,len(b)):
        if i%22==0:         # need multiple of 11
            c.append(b[i])
            d.append(data[i,1])
    
    plt.plot(d , c , "x-" ,label = "Surface Energy = " + str(gammas[a]))
    #plt.plot(data[:,1],p_c*data[:,2], 'x', label = "Surface Energy = " + str(gammas[a]))
plt.legend()
plt.show()

fig1.savefig('/Users/Noah/python/tapping_packing/filling/' + variable + "gamma2"+ str(gammas[0])
             +"to"+str(gammas[-1])+'.png', dpi=400, bbox_inches="tight")




