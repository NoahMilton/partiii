# required arguments
# thisfile.py filestem no.of.files
# where filestem is of the form e.g. 'force_jrkpw_variable_'
# no.of.files is the number of .csv files to be analysed e.g. '10'

# note requirement for this .py script to be located in the same directory as the 
# desired .csv files

"""
Would like to be able to extract the maximum rebound velocity and input velocity
to calculate the coefficient of restitution for several simulations.
Then it should be easy enough to run multiple simulations (e.g. with varying
initial velocities) and test if the input coefficient of restitution is equal
to the measured value for each force model.
"""
import sys
import os
import numpy as np

filestem = sys.argv[1]  # stem of the file name up to the number
N = int(sys.argv[2])    # Number of source files to be analysed


def coeffofr(filex):
    #outputs initial speed and corresponding coefficient of restitution
    
    with open(filex, 'r') as fd_file:
    	header = fd_file.readline()    # this line supposedly not used but seems necessary
    	fd = [line.strip() for line in fd_file]
    
    speed = np.array([np.float64(line.split(",")[4]) for line in fd])
    
    e = max(speed)/abs(speed[0])
    
    print(speed[0],',',e)
    return (speed[0],e);


coeffs = []    
i = 1 

print('start velocity, coeff of restitution')

while i < N+1:
    j = str(i)
    coeffs.append(coeffofr(os.getcwd() +'/' +filestem + j + '.csv'))
    i +=1
    
