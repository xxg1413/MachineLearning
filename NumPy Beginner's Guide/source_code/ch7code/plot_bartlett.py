import numpy as np
from matplotlib.pyplot import plot, show

window = np.bartlett(42)
plot(window)
show()
