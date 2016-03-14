import numpy as np

# Chapter2 Beginning with NumPy fundamentals
#
# Demonstrates the NumPy 
# dtype attributes
#
# Run from the commandline with 
#
#  python dtypeattributes2.py
print "In: t = dtype('Float64')"
t = np.dtype('Float64')

print "In: t.char"
print t.char
#Out: 'd'

print "In: t.type"
print t.type
#Out: <type 'numpy.float64'>

print "In: t.str"
print t.str
#Out: '<f8'



