import numpy as np

# Chapter 2 Beginning with NumPy fundamentals
#
# Demonstrates the NumPy dtype constructors.
#
# Run from the commandline with 
#
#  python dtypeconstructors.py
print "In: dtype(float)"
print np.dtype(float)
#Out: dtype('float64')

print "In: dtype('f')"
print np.dtype('f')
#Out: dtype('float32')


print "In: dtype('d')"
print np.dtype('d')
#Out: dtype('float64')

print "In: dtype('f8')"
print np.dtype('f8')
#Out: dtype('float64')


print "In: dtype('Float64')"
print np.dtype('Float64')
#Out: dtype('float64')

