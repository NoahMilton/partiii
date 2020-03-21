import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import os
# import try_2 as rl
# import scipy.interpolate
# import cPickle as pickle
import sys
# from scipy.special import factorial
# from scipy.optimize import curve_fit
# from scipy.optimize import fsolve
# from scipy.integrate import simps
import seaborn as sns
plt.style.use('bmh')
#sns.palplot(sns.color_palette("Paired"))
#sns.set(style="white", palette="deep", color_codes=True)
#sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = 'true'
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 8
plt.rcParams['lines.markeredgewidth'] = 1
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['font.size'] = 12
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
# Get current size
fig_size = plt.rcParams["figure.figsize"]

inputfile = sys.argv[1] # Input file to plot, as a csv
# print matplotlib.__version__
with open(inputfile, 'r') as fd_file:
	header = fd_file.readline()
	fd = [line.strip() for line in fd_file]
time = np.array([np.float64(line.split(",")[0]) for line in fd])
distant = np.array([np.float64(line.split(",")[1]) for line in fd])
forces = np.array([np.float64(line.split(",")[2]) for line in fd])
overlaps = np.array([np.float64(line.split(",")[3]) for line in fd])
speed = np.array([np.float64(line.split(",")[4]) for line in fd])
f = plt.figure(1)
# plt.ion()
plt.plot(time,abs(speed), '+r',label = 'vel')
plt.xlabel("Time [s]")
plt.ylabel("Velocity [m/s]")
f = plt.figure(2)
plt.plot(overlaps*1e6,forces*1000, '+r',label = 'F_n')
plt.xlabel("Overlap [um]")
plt.ylabel("Force [mN]")
# plt.ion()
fig, ax1 = plt.subplots()
fig_size = plt.rcParams["figure.figsize"]
color = 'tab:red'
ax1.set_ylabel("Overlap [um]")
ax1.set_xlabel("Time [s]")
ax1.plot(time,overlaps*1e6, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel("Force [mN]", color=color)  # we already handled the x-label with ax1
ax2.plot(time, forces*1000, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
#plt.xlim(-0.1*max(overlaps*1e6),max(overlaps*1e6))
#plt.ylim(min(forces*1000),max(forces*1000))
# plt.grid()


#plt.legend(frameon=True,loc = 0)
#plt.grid(False)
plt.show()
