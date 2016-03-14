import numpy as np

data = np.eye(2)
np.savetxt("eye.txt", data)
print np.genfromtxt("eye.txt")
