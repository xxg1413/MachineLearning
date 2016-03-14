import numpy as np
from matplotlib.pyplot import plot, show

x =  np.linspace(0, 2 * np.pi, 30)
wave = np.cos(x)
transformed = np.fft.fft(wave)
shifted = np.fft.fftshift(transformed)
print np.all(np.abs(np.fft.ifftshift(shifted) - transformed) < 10 ** -9)

plot(transformed, lw=2)
plot(shifted, lw=3)
show()
