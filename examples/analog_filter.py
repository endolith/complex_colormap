"""
Analyze signal processing filters
"""

import numpy as np
from complex_colormap.cplot import cplot
from scipy.signal import butter, freqs_zpk
import matplotlib.pyplot as plt

f_c = 100  # rad/s
r = 200  # rad/s

z, p, k = butter(3, f_c, btype='hp', analog=True, output='zpk')


def splane_eval(s):
    """
    `s` is a value on the analog S plane.  The frequency response at 10 Hz
    would be s = 1j*2*pi*10, for instance.
    """
    return freqs_zpk(z, p, k, -1j * s)[1]


gridspec_kw = {'width_ratios': [3, 1, 1]}
fig, (ax_cplot, ax_fr, ax_ph) = plt.subplots(1, 3, sharey=True,
                                             figsize=(8.8, 5),
                                             gridspec_kw=gridspec_kw)
cplot(splane_eval, re=(-r, r), im=(-r, r), axes=ax_cplot)
ax_cplot.set_xlabel('$\sigma$')
ax_cplot.set_ylabel('$j \omega$')
ax_cplot.axhline(0, color='white', alpha=0.15)
ax_cplot.axvline(0.5, color='white', alpha=0.15)
ax_cplot.set_title('S plane')
ax_cplot.axis('equal')

w, h = freqs_zpk(z, p, k, np.linspace(-r, r, 500))

ax_fr.plot(abs(h), w)
ax_fr.invert_xaxis()
ax_fr.tick_params(axis='y', left='off', right='on')
ax_fr.set_xlabel('Magnitude')
ax_fr.grid(True, which='both')

ax_ph.plot(np.rad2deg(np.angle(h)), w)
ax_ph.invert_xaxis()
ax_ph.tick_params(axis='y', left='off', right='on', labelright='on')
ax_ph.set_xlabel('Phase [degrees]')
ax_ph.set_ylabel('Frequency [rad/s]')
ax_ph.yaxis.set_label_position("right")
ax_ph.grid(True, which='both')
ax_ph.margins(0.05, 0)

plt.tight_layout()
