#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:31:01 2019

@author: Noah
"""
""" plotting the RDF of a simulated packing system, using the compute rdf
function in LIGGGHTS """

import numpy as np
import matplotlib.pyplot as plt

plot_X_Fu = 1
#variable = yieldStress
#rep1=(0.1 1 5 10 100)

# Vairables to Change before running
test = "TN_region_test"  # test name for output file
rowstoskip = 4      # row (x value) to start reading data from, minimum 4
filestem = str("/Users/Noah/remote/LIGGGHTS/Run/ContactModel/" + 
    "packing/thornton_ning_test/small_particles/basecase/")

radius = 0.2*(10**-3)   # average radius in simulation for normalising

rdfdata = np.loadtxt(filestem + "rdfoutput.txt", skiprows=rowstoskip)
norm_radius = rdfdata[:,1]/(2*radius) ;  # normalise radial distance using radius
rdf = rdfdata[:,2];

fig = plt.figure()   # do the figure
plt.xlabel("r/<D>")
plt.ylabel("g(r)")
plt.plot(norm_radius, rdf, label = str(test))


if plot_X_Fu == 1:
    x, y = np.loadtxt('/Users/Noah/python/RDF/data/X_Fu_monodisperse_normalised.csv',
                      delimiter=',', unpack=True)
    plt.plot(x,y, label = "X. Fu et al.")
else:
    print("Not plotting data from X_Fu...")


plt.legend()
#fig.savefig('RDF_'+test+'.png', dpi=400)



#### NOW TACKEL THE COORDINATION NUMBER ####
filename = str(filestem + "post/coordination.txt")

# Find the number of particles so we only extract one timestep's worth
with open(filename) as myfile:  
    head = [next(myfile) for x in range(3)]
x = head[1].split("\t")
n_particle = int(str(x[1]).rstrip("\n"))\

# Now import coordination number data from row 3 down to n_particle
coordata = np.loadtxt(filename, skiprows=3, max_rows=n_particle)

# Calculate average coordination number and standard deviation
av = np.average(coordata)
std = np.std(coordata)

print("Average coordination number = " + str(av)[:5] + "\n" + "StDev = " + str(std)[:5])
