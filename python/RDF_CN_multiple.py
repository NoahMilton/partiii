#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 17:39:15 2020

@author: Noah
"""

import numpy as np
import matplotlib.pyplot as plt

variable = "COR"
variablelabel = "GDC"
unit = ""
plot_X_Fu = 1       # yes = 1, no = 0

N = 6  # number of variable values to load runs for

radius = 0.1*(10**-3)   # average radius in simulation for normalising

filestem = str("/Users/Noah/remote/LIGGGHTS/Run/ContactModel/" + 
               "packing/thornton_ning_test/small_particles/"+ variable + "/" )#+'/narrowed_search2/')

# Let's get the values from the bash output file
values = np.loadtxt(filestem + "variables.txt", skiprows=2)
print("\n" + "Using " + variable + " values of " + str(values) + "\n")

# now find the .csv files for this investigation
filelist = []
coordfilelist = []
rowstoskip = 5      # row to start reading data from for rdf, minimum 4

#values = np.delete(values, [0])

for i in range(1,N+1):      # make a list of files to enter for RDF and COOrd.
    number = str(i).zfill(2)
    filelist.append(filestem + variable + "_" + number + "/rdfoutput.txt")
    coordfilelist.append(filestem  + variable + "_" + number + "/post/coordination.txt")

fig1 = plt.figure(1)   # set up first figure
plt.xlabel("r/<D>")
plt.ylabel("g(r)")
plt.title("RDF")

# Read in and plot X. Fu et al data (normalised to finish at 1)
if plot_X_Fu == 1:
    x, y = np.loadtxt('/Users/Noah/python/RDF/data/X_Fu_monodisperse_normalised.csv',
                      delimiter=',', unpack=True)
    plt.plot(x,y, label = "X. Fu et al.")
else:
    print("Not plotting data from X_Fu...")
    

for fname in filelist:      # plot data from each RDF file
    rdfdata = np.loadtxt(fname, skiprows=rowstoskip)
    norm_radius = rdfdata[:,1]/(2*radius) ;  # normalise radial distance using radius
    rdf = rdfdata[:,2];
    rdf_2 = rdf/rdf[-1]
    a = filelist.index(fname)
    plt.plot(norm_radius, rdf_2, label = variablelabel + " = " + str(values[a]))
    plt.legend()
    

fig1.savefig('RDF_TN_' + variable + str(values[0])+ "_to_" + str(values[-1]) + "_" + str(N) + '.png', dpi=400)



#### NOW TACKEL THE COORDINATION NUMBER ####
# Find the number of particles so we only extract one timestep's worth
coordination = []
coordination_stdev = []

for fname in coordfilelist:
    with open(fname) as myfile:
        head = [next(myfile) for x in range(3)]
        x = head[1].split("\t")
        n_particle = int(str(x[1]).rstrip("\n"))
    
    # Now import coordination number data from row 3 down to n_particle
    coordata = np.loadtxt(fname, skiprows=3, max_rows=n_particle)

    # Calculate average coordination number and standard deviation
    av = np.average(coordata)
    std = np.std(coordata)
    # Print and save to file
    a = coordfilelist.index(fname)
    coordination.append(av)
    coordination_stdev.append(std)
    print(variable + " = " + str(values[a]))
    print("\t"+"Average coordination number = " + str(av)[:5] + "\n\t" + "StDev = " + str(std)[:5])

fig2 = plt.figure(2)   # Plot the coordination number
plt.ylabel("Coordination Number")
plt.xlabel(variablelabel + unit)
plt.title("Coordination Number")
#plt.ylim(bottom=0, top =8)      # set limits
#plt.errorbar(values[:len(coordination)],coordination, 
#          fmt = 'x', yerr = coordination_stdev)      # plot with errors
plt.plot(values[:len(coordination)],coordination,'x')
plt.show()

fig2.savefig('/Users/Noah/python/Coordination_No/CN_' + variable + str(values[0])+ "_to_" +
             str(values[-1]) + "_" + str(N) + '.png', dpi=400)
                 
                 
                