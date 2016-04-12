from numpy import *

def difcost(a,b):
  dif=0
  for i in range(shape(a)[0]):
    for j in range(shape(a)[1]):
      # Euclidean Distance
      dif+=pow(a[i,j]-b[i,j],2)
  return dif

def factorize(v,pc=10,iter=50):
  ic=shape(v)[0]
  fc=shape(v)[1]

  # Initialize the weight and feature matrices with random values
  w=matrix([[random.random() for j in range(pc)] for i in range(ic)])
  h=matrix([[random.random() for i in range(fc)] for i in range(pc)])

  # Perform operation a maximum of iter times
  for i in range(iter):
    wh=w*h
    
    # Calculate the current difference
    cost=difcost(v,wh)
    
    if i%10==0: print cost
    
    # Terminate if the matrix has been fully factorized
    if cost==0: break
    
    # Update feature matrix
    hn=(transpose(w)*v)
    hd=(transpose(w)*w*h)
  
    h=matrix(array(h)*array(hn)/array(hd))

    # Update weights matrix
    wn=(v*transpose(h))
    wd=(w*h*transpose(h))

    w=matrix(array(w)*array(wn)/array(wd))  
    
  return w,h
