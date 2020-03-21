" Calculates coefficient of restitution for a set of files based on initial "
" velocities and maximum return speeds " 
" Outputs a text file with velocity and COR, which can then be plot "
" CORs'filestem'_'number of values'.txt "

# required arguments
# thisfile.py filestem no.of.files
# where filestem is of the form e.g. 'force_jrkpw_variable_'
# no.of.files is the number of .csv files to be analysed e.g. '10'

# note requirement for this .py script to be located in the same directory as the 
# desired .csv files

import sys
import os
import numpy as np

filestem = sys.argv[1]  # stem of the file name up to the number
N = int(sys.argv[2])    # Number of source files to be analysed
testname = sys.argv[3]  # Name of test to append to CORs text file

output = open("CORs"+ filestem + str(N) + testname + ".txt","w+")
print('start velocity, coeff of restitution\n')

i=1
while i < N+1:
    j = str(i).zfill(2)
    filex = os.getcwd()+'/'+filestem + j + '.csv'
    with open(filex, 'r') as fd_file:   
    	header = fd_file.readline()    # this line supposedly not used but seems necessary
    	fd = [line.strip() for line in fd_file]
    speed = np.array([np.float64(line.split(",")[4]) for line in fd])
    e = speed[-1]/abs(speed[0])
    
    print(speed[0],',',e)
    sp = str(speed[0])
    cor = str(e)
    output.write('{0} {1}\n'.format(sp, cor))
    #coeffs.append(speed[0] e)
    
    i +=1
