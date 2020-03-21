#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 22:10:41 2020

Computes and plots Contact force info (Contact and Normal), average overlap, 
average height, average coordinatino number (CN) and the radial distribution function (RDF),
for tests of different parameter values, when given the variable name as used
in LIGGGHTS simulations.

Script sections are:
1: Define inputs, extract data and perform necessary calculations       (slow)
2: Remove results associated with useless variable values (too high/small/etc)  (fast)
3: Plot data stored in local variables              (fast)
4: Save figues using variable name and range of variable values

@author: Noah
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scp
import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter



def contact_forces(fname):
    # Input file stem up to and including /variable_0i/
    # Returns contact_info = (c_force, n_force, t_force, delta)
    allcforces = np.loadtxt(fname + "post/contact_force.txt", skiprows=3)#, max_rows = 1000)
    allnforces = np.loadtxt(fname + "post/force_normal.txt", skiprows=3)
    alltforces = np.loadtxt(fname + "post/force_tangential.txt", skiprows = 3)
    alldelta = np.loadtxt(fname + "post/delta.txt", skiprows = 3)
    indices = np.nonzero(allcforces)

    indices_no_dup = [] 
    for i in indices[0]: # remove duplicate indices to select only one row
        if i not in indices_no_dup: 
            indices_no_dup.append(i)

    # Select only the non-zero force elements
    cforces = allcforces[indices_no_dup,:]
    nforces = allnforces[indices_no_dup,:]
    tforces = alltforces[indices_no_dup,:]
    delta = alldelta[indices_no_dup]

    # Sum force components to get overall force
    c_force = np.zeros((len(cforces),1))
    n_force = np.zeros((len(nforces),1))
    t_force = np.zeros((len(tforces),1))

    for i in range(0,len(cforces)):     # combine x, y, & z force components
        c_force[i] = (10**6)*np.sqrt(cforces[i,0]**2 + cforces[i,1]**2 + cforces[i,2]**2)
        n_force[i] = (10**6)*np.sqrt(nforces[i,0]**2 + nforces[i,1]**2 + nforces[i,2]**2)
        t_force[i] = np.sqrt(tforces[i,0]**2 + tforces[i,1]**2 + tforces[i,2]**2)

    contact_info = (c_force, n_force, t_force, delta)
    return contact_info

def average_z(fname):
    # Calculate the average height using this file stem up to and including /post/
    z_data = np.loadtxt(fname + "post/height.txt", skiprows = 3)
    av = np.average(z_data)
    std = np.std(z_data)
    b = (av, std)
    return b

"""
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   
"""
# Inputs
variable = "scalefactor"
variablelabel = "Scale Factor"
unit = ""
errors = 1          # Error bars:   on = 1, off = 0 
plot_X_Fu = 0       # X. Fu data:   on = 1, off = 0

# Make a list of file locations
filelist = []
rdffilelist = []
coordfilelist = []

# Initialise lists to be plot later
c_force = []
n_force = []
t_force = []
average_cforce = []
average_nforce = []
av_delta = []
delta_err = []
z_av = []
z_std = []
coordination = []
coordination_stdev = []
RDFs = []

p_size = 200e-6 # Particle diameter for delta and z
radius = p_size/2

#filestem = str("/Users/Noah/remote/LIGGGHTS/Run/ContactModel/" + 
 #              "packing/thornton_ning_test/small_particles/" + variable + "/")
filestem = str("/Users/Noah/remote/LIGGGHTS/Run/ContactModel/" + 
               "packing/forced_packing/wiggle/scaling_tests/full_scale/no_tapping/" + variable + "/")

# Get parameter values
values = np.loadtxt(filestem + "variables.txt", skiprows=1)
N = int(values[0])      # Number of variable cases to load
values = np.delete(values,[0])

print("\n" + "Loading " + str(N) + " values of " + variable + " : " + str(values) + "\n")

# Make lists of files to load
for i in range(1,N+1):
    trial_no = str(i).zfill(2)
    filelist.append(filestem + variable + "_" + trial_no + "/")
    rdffilelist.append(filestem + variable + "_" + trial_no + "/rdfoutput.txt")
    coordfilelist.append(filestem  + variable + "_" + trial_no + "/post/coordination.txt")
print("\n" + "Wait for data extraction ..." + "\n")

## Contact force, Normal Force, Tangential Force, Delta
for i in range(len(filelist)):  # Get data from files, remove 0 values
    X = contact_forces(filelist[i])
    c_force.append(X[0])
    n_force.append(X[1])
    t_force.append(X[2])
    delta = X[3]
    
    av_delta.append(np.average(delta)*100/(p_size*values[i]**0.4)) # delta overlap in %
    delta_err.append((np.std(delta)*100/(p_size*values[i]**0.4))/np.sqrt(len(delta)))
    average_cforce.append(np.average(c_force[i]))
    average_nforce.append(np.average(n_force[i]))

## Average Height, into z_av and z_std
for i in range(len(filelist)):
    z = average_z(filelist[i])
    z_av.append(z[0]/(p_size*values[i]**0.4))
    z_std.append(z[1]/(p_size*values[i]**0.4))

## Coordination Number, into list 'coordination' and 'coordination_stdev'
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
    #print(variable + " = " + str(values[a]))
    #print("\t"+"Average coordination number = " + str(av)[:5] + "\n\t" + "StDev = " + str(std)[:5])

## RDF, into list 'RDFs'
for fname in rdffilelist:
    rdfdata = np.loadtxt(fname, skiprows=5)
    a = rdffilelist.index(fname)
    norm_radius = rdfdata[:,1]/(2*radius*values[a]**0.4) ;  # normalise radial distance using radius
    rdf = rdfdata[:,2];
    rdf_2 = rdf/rdf[-1]    # set RDF to be 1 at 6 x diameter
    #a = rdffilelist.index(fname)
    RDFs.append(rdf_2)

run_no = 0
print("... data extraction complete.")
#%% Data Selection / Manipulation
# Change if you don't want to plot all parameter runs

remove_end = 1          # remove from high end
remove_beginning = 0    # remove from low end

if run_no < 1 :        # Ensure nothing removed on first run:
    remove_end = 0
    remove_beginning = 0

if remove_end > 0:
    for i in range (remove_end):
        #for item in lists:
            #    item = np.delete(item, [len(item)])    
        final_index = len(values) - 1
        values = np.delete(values,[final_index])
        av_delta = np.delete(av_delta,[final_index])
        c_force = np.delete(c_force,[final_index])
        n_force = np.delete(n_force,[final_index])
        t_force = np.delete(t_force,[final_index])
        coordination = np.delete(coordination,[final_index])
        coordination_stdev = np.delete(coordination_stdev,[final_index])
        average_cforce = np.delete(average_cforce,[final_index])
        average_nforce = np.delete(average_nforce,[final_index])
        z_av = np.delete(z_av,[final_index])
        z_std = np.delete(z_std,[final_index])
        RDFs = np.delete(RDFs, [final_index], 0)
        print("Index number " + str(final_index) + " removed")
        
if remove_beginning > 0:
    for i in range (remove_beginning):
        #for item in lists:
            #    item = np.delete(item, [len(item)])    
        final_index = i
        values = np.delete(values,[final_index])
        av_delta = np.delete(av_delta,[final_index])
        c_force = np.delete(c_force,[final_index])
        n_force = np.delete(n_force,[final_index])
        t_force = np.delete(t_force,[final_index])
        coordination = np.delete(coordination,[final_index])
        coordination_stdev = np.delete(coordination_stdev,[final_index])
        average_cforce = np.delete(average_cforce,[final_index])
        average_nforce = np.delete(average_nforce,[final_index])
        z_av = np.delete(z_av,[final_index])
        z_std = np.delete(z_std,[final_index])
        RDFs = np.delete(RDFs,[final_index])
        print("Index number " + str(i) + " removed")

N = len(values)     # to correct for labelling
run_no = run_no + 1
print("Data selection complete, remaining values are: \n" + str(values))
#%%
## Plotting ##
if errors == 1:
    errortext = "err"
else:
    errortext = ""
    
print("\n" + "Plotting...")
bin_no = 100
fig1 = plt.figure(1)   # Contact Force PDF
plt.ylabel("Probability Density")
plt.xlabel("Force Magnitude (x10^6 N)")
plt.title("Contact Force PDF")

fig2 = plt.figure(2)    # Normal Force PDF
plt.ylabel("Probability Density")
plt.xlabel("Force Magnitude (x10^6 N)")
plt.title("Normal Force PDF")

for i in range(len(values)):  # Plot the PDFs - semilogx
    plt.figure(1)       # Contact Force
    x_cf = np.linspace(0, max(c_force[i]), bin_no) # NB should plot wrt c_force[i]
    hist_cf = np.histogram(c_force[i], bins=bin_no)
    c_force_dist = scp.rv_histogram(hist_cf)
    plt.semilogx(x_cf, c_force_dist.pdf(x_cf), label = variablelabel + " = " + str(values[i]))

    plt.figure(2)       # Normal Force
    x_nf = np.linspace(0, max(n_force[i]), bin_no) # NB should plot wrt c_force[i]
    hist_nf = np.histogram(n_force[i], bins=bin_no)
    n_force_dist = scp.rv_histogram(hist_nf)
    plt.semilogx(x_nf, n_force_dist.pdf(x_nf), label = variablelabel + " = " + str(values[i]))
    
plt.figure(1)
plt.legend()
plt.figure(2)
plt.legend()

fig4 = plt.figure(4)    # Contact and Normal Force Magnitudes
plt.ylabel("Average Force (x10^6 N)")
plt.xlabel(variablelabel + unit)
plt.title("Total Contact Force and Normal Force")
plt.plot(values, average_cforce, 'x', label = "Contact force")
plt.plot(values, average_nforce, '.', label = "Normal force")
plt.legend()
plt.show()

fig3 = plt.figure(3)    # Overlap
plt.ylabel("Overlap (% average particle diameter)")
plt.title("Average Particle Overlap")
plt.xlabel(variablelabel + unit)
if errors ==1:
    plt.errorbar(values, av_delta, fmt = 'x', yerr = delta_err, elinewidth = 1, capsize = 1, label = "Average Overlap")
else:
    plt.plot(values, av_delta, 'x', label = "Average Overlap")
plt.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0,0))    
plt.show

fig5 = plt.figure(5)    # Particle Height
plt.ylabel("Height (particle diameters)")
plt.xlabel(variablelabel + unit)
plt.title("Average Particle Height")
z_err = z_std/np.sqrt(n_particle)

plt.ylim(11, 12)

if errors == 1:
    plt.errorbar(values, z_av, fmt = 'x', yerr = z_err, elinewidth = 1, capsize = 1)
else:
    plt.plot(values, z_av, 'x')
plt.show()

fig6 = plt.figure(6)    #RDF
plt.xlabel("r/<D>")
plt.ylabel("g(r)")
plt.title("RDF")

if plot_X_Fu == 1:  # Read in and plot X. Fu et al data (normalised to finish at 1)
    plt.figure(6)
    x, y = np.loadtxt('/Users/Noah/python/RDF/data/X_Fu_monodisperse_normalised.csv',
                      delimiter=',', unpack=True)
    plt.plot(x,y, label = "X. Fu et al.")
    Fu = "_Fu"
else:
    print("Not plotting data from X_Fu...")
    Fu = ""
for i in range(len(values)):
    plt.figure(6)
    plt.plot(norm_radius, RDFs[i], label = variablelabel + " = " + str(values[i]))
    plt.legend()
    
fig7 = plt.figure(7)   # Coordination number
plt.ylabel("Coordination Number")
plt.xlabel(variablelabel + unit)
plt.title("Coordination Number")

ax = plt.gca()
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.ylim(6, 6.2)
coordination_err = coordination_stdev/np.sqrt(n_particle)
if errors == 1:
    plt.errorbar(values[:len(coordination)],coordination, fmt = 'x', yerr = coordination_err, elinewidth = 1, capsize = 1)
else:
    plt.plot(values[:len(coordination)],coordination,'x')


plt.show()


#%%     ## Save the Figures
print("\n" + "Plotting complete, saving figures...")

fig1.savefig('/Users/Noah/python/tapping_packing/' + 'cF_' + variable + str(values[0]) +
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + '.png', dpi=400)

fig2.savefig('/Users/Noah/python/tapping_packing/' + 'nF_' + variable +  str(values[0]) +
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + '.png', dpi=400)

fig3.savefig('/Users/Noah/python/tapping_packing/' + 'delta_' + variable + str(values[0]) +
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + errortext + '.png', dpi=400)

fig4.savefig('/Users/Noah/python/tapping_packing/' + 'cF_nF_' + variable + str(values[0]) +
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + '.png', dpi=400)

fig5.savefig('/Users/Noah/python/tapping_packing/' + 'z_' + variable + str(values[0]) +
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + errortext + '.png', dpi=400)

fig6.savefig('/Users/Noah/python/tapping_packing/' + 'RDF_' + variable + str(values[0])+ 
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + '.png', dpi=400)

fig7.savefig('/Users/Noah/python/tapping_packing/' + 'CN_' + variable + str(values[0])+ 
             "_to_" + str(values[-1]) + "_" + str(N) + Fu + errortext + '.png', dpi=400)

print("\nSaved to /Users/Noah/python/gravity_packing/")