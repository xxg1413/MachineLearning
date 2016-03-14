import numpy as np

A = np.mat("3 -2;1 0")
print "A\n", A

print "Eigenvalues", np.linalg.eigvals(A) 

eigenvalues, eigenvectors = np.linalg.eig(A)
print "First tuple of eig", eigenvalues
print "Second tuple of eig\n", eigenvectors

for i in range(len(eigenvalues)):
      print "Left", np.dot(A, eigenvectors[:,i])
      print "Right", eigenvalues[i] * eigenvectors[:,i]
      print
