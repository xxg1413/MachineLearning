import numpy as np
from matplotlib.pyplot import plot, show

points = np.zeros(100)
outcomes = np.random.hypergeometric(25, 1, 3, size=len(points))

for i in range(len(points)):
   if outcomes[i] == 3:
      points[i] = points[i - 1] + 1
   elif outcomes[i] == 2:
      points[i] = points[i - 1] - 6
   else:
      print outcomes[i]

plot(np.arange(len(points)), points)
show()
