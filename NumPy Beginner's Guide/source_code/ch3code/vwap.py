import numpy as np

c,v=np.loadtxt('data.csv', delimiter=',', usecols=(6,7), unpack=True)
vwap = np.average(c, weights=v)
print "VWAP =", vwap

print "mean =", np.mean(c)

t = np.arange(len(c))
print "twap =", np.average(c, weights=t)
