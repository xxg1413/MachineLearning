import numpy as np

# Chapter 2 Beginning with NumPy fundamentals
#
# Demonstrates multi dimensional arrays slicing.
#
# Run from the commandline with 
#
#  python shapemanipulation.py
print "In: b = arange(24).reshape(2,3,4)"
b = np.arange(24).reshape(2,3,4)

print "In: b"
print b
#Out: 
#array([[[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]],
#
#       [[12, 13, 14, 15],
#        [16, 17, 18, 19],
#        [20, 21, 22, 23]]])

print "In: b.ravel()"
print b.ravel()
#Out: 
#array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
#       17, 18, 19, 20, 21, 22, 23])

print "In: b.flatten()"
print b.flatten()
#Out: 
#array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
#       17, 18, 19, 20, 21, 22, 23])

print "In: b.shape = (6,4)"
b.shape = (6,4)

print "In: b"
print b
#Out: 
#array([[ 0,  1,  2,  3],
#       [ 4,  5,  6,  7],
#       [ 8,  9, 10, 11],
#       [12, 13, 14, 15],
#       [16, 17, 18, 19],
#       [20, 21, 22, 23]])

print "In: b.transpose()"
print b.transpose()
#Out: 
#array([[ 0,  4,  8, 12, 16, 20],
#       [ 1,  5,  9, 13, 17, 21],
#       [ 2,  6, 10, 14, 18, 22],
#       [ 3,  7, 11, 15, 19, 23]])


print "In: b.resize((2,12))"
b.resize((2,12))

print "In: b"
print b
#Out: 
#array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11],
#       [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]])

