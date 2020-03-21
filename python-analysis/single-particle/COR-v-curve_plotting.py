#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 15:49:46 2019

@author: Noah
"""

import matplotlib.pyplot as plt
import sys

i=1
filex = sys.argv[i]
#filex = "CORsmodulus_03vel_99.txt"

plt.xlabel("Velocity [m/s]")
plt.ylabel("Coefficient of Restitution")

X, Y = [], []

N=2
while i < N:
    for line in open(filex, 'r'):
      values = [float(s) for s in line.split()]
      X.append(abs(values[0]))
      Y.append(values[1])
      plt.plot(X,Y)
#plt.plot(X, Y)
#plt.scatter(X, Y)
#plt.show()
