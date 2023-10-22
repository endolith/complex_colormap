# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from complex_colormap.cplot import const_chroma_colormap_mpl

# size
N = 512
# frequency
f = 1
# whether to use amplitude modulation (bool)
AM = 0

# make sine
t = np.arange(N)/N
x = np.cos(2*np.pi*f*t) + 1j*np.sin(2*np.pi*f*t)
x = np.repeat(x[None], N, 0)
if AM:
    x *= t[::-1]

# plot
cm = const_chroma_colormap_mpl(N)
plt.imshow(np.angle(x), alpha=np.abs(x)**(1/2), cmap=cm,
           interpolation='nearest', aspect='auto')
# (other interpolations tend to produce artifacts per phase jump)
