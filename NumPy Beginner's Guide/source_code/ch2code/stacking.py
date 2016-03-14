import numpy as np

# Chapter 2 Beginning with NumPy fundamentals
#
# Demonstrates array stacking.
#
# Run from the commandline with 
#
#  python stacking.py
print "In: a = arange(9).reshape(3,3)"
a = np.arange(9).reshape(3,3)

print "In: a"
print a
#Out: 
#array([[0, 1, 2],
#       [3, 4, 5],
#       [6, 7, 8]])

print "In: b = 2 * a"
b = 2 * a

print "In: b"
print b
#Out: 
#array([[ 0,  2,  4],
#       [ 6,  8, 10],
#       [12, 14, 16]])

print "In: hstack((a, b))"
print np.hstack((a, b))
#Out: 
#array([[ 0,  1,  2,  0,  2,  4],
#       [ 3,  4,  5,  6,  8, 10],
#       [ 6,  7,  8, 12, 14, 16]])

print "In: concatenate((a, b), axis=1)"
print np.concatenate((a, b), axis=1)
#Out: 
#array([[ 0,  1,  2,  0,  2,  4],
#       [ 3,  4,  5,  6,  8, 10],
#       [ 6,  7,  8, 12, 14, 16]])

print "In: vstack((a, b))"
print np.vstack((a, b))
#Out: 
#array([[ 0,  1,  2],
#       [ 3,  4,  5],
#       [ 6,  7,  8],
#       [ 0,  2,  4],
#       [ 6,  8, 10],
#       [12, 14, 16]])

print "In: concatenate((a, b), axis=0)"
print np.concatenate((a, b), axis=0)
#Out: 
#array([[ 0,  1,  2],
#       [ 3,  4,  5],
#       [ 6,  7,  8],
#       [ 0,  2,  4],
#       [ 6,  8, 10],
#       [12, 14, 16]])

print "In: dstack((a, b))"
print np.dstack((a, b))
#Out: 
#array([[[ 0,  0],
#        [ 1,  2],
#        [ 2,  4]],
#
#       [[ 3,  6],
#        [ 4,  8],
#        [ 5, 10]],
#
#       [[ 6, 12],
#        [ 7, 14],
#        [ 8, 16]]])

print "In: oned = arange(2)"
oned = np.arange(2)

print "In: oned"
print oned
#Out: array([0, 1])

print "In: twice_oned = 2 * oned"
twice_oned = 2 * oned

print "In: twice_oned"
print twice_oned
#Out: array([0, 2])

print "In: column_stack((oned, twice_oned))"
print np.column_stack((oned, twice_oned)) 
#Out: 
#array([[0, 0],
#       [1, 2]])

print "In: column_stack((a, b))"
print np.column_stack((a, b))
#Out: 
#array([[ 0,  1,  2,  0,  2,  4],
#       [ 3,  4,  5,  6,  8, 10],
#       [ 6,  7,  8, 12, 14, 16]])

print "In: column_stack((a, b)) == hstack((a, b))"
print np.column_stack((a, b)) == np.hstack((a, b))
#Out: 
#array([[ True,  True,  True,  True,  True,  True],
#       [ True,  True,  True,  True,  True,  True],
#       [ True,  True,  True,  True,  True,  True]], dtype=bool)

print "In: row_stack((oned, twice_oned))"
print np.row_stack((oned, twice_oned))
#Out: 
#array([[0, 1],
#       [0, 2]])
 
print "In: row_stack((a, b))"
print np.row_stack((a, b))
#Out: 
#array([[ 0,  1,  2],
#       [ 3,  4,  5],
#       [ 6,  7,  8],
#       [ 0,  2,  4],
#       [ 6,  8, 10],
#       [12, 14, 16]])

print "In: row_stack((a,b)) == vstack((a, b))"
print np.row_stack((a,b)) == np.vstack((a, b))
#Out: 
#array([[ True,  True,  True],
#       [ True,  True,  True],
#       [ True,  True,  True],
#       [ True,  True,  True],
#       [ True,  True,  True],
#       [ True,  True,  True]], dtype=bool)

