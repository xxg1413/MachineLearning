import numpy as np
from matplotlib.pyplot import plot, show

x =  np.linspace(0, 2 * np.pi, 30)
wave = np.cos(x)
transformed = np.fft.fft(wave)
print np.all(np.abs(np.fft.ifft(transformed) - wave) < 10 ** -9)

plot(transformed)
show()
