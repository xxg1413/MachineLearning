import numpy as np
from matplotlib.pyplot import plot, show

x = np.linspace(0, 4, 100)
vals = np.sinc(x)

plot(x, vals)
show()
