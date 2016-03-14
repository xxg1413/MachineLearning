#!/usr/bin/env/python

import sys
from datetime import datetime
import numpy as np

"""
 Chapter 1 of NumPy Beginners Guide.
 This program demonstrates vector addition the Python way.
 Run from the command line as follows
     
  python vectorsum.py n
 
 where n is an integer that specifies the size of the vectors.

 The first vector to be added contains the squares of 0 up to n. 
 The second vector contains the cubes of 0 up to n.
 The program prints the last 2 elements of the sum and the elapsed time.
"""

def numpysum(n):
   a = np.arange(n) ** 2
   b = np.arange(n) ** 3
   c = a + b

   return c

def pythonsum(n):
   a = range(n)
   b = range(n)
   c = []

   for i in range(len(a)):
       a[i] = i ** 2
       b[i] = i ** 3
       c.append(a[i] + b[i])

   return c
   

size = int(sys.argv[1])

start = datetime.now()
c = pythonsum(size)
delta = datetime.now() - start
print "The last 2 elements of the sum", c[-2:]
print "PythonSum elapsed time in microseconds", delta.microseconds

start = datetime.now()
c = numpysum(size)
delta = datetime.now() - start
print "The last 2 elements of the sum", c[-2:]
print "NumPySum elapsed time in microseconds", delta.microseconds
