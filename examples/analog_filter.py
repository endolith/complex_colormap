"""
Generate analog signal processing filter, showing:
    Poles and zeros using complex colormap
    Magnitude and phase frequency response plots on linear-linear axes
    Magnitude plot on more typical log-log plot
"""

import numpy as np
from complex_colormap.cplot import cplot
from scipy.signal import butter, freqs_zpk
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

f_c = 100  # rad/s
r = 200  # rad/s

z, p, k = butter(3, f_c, btype='hp', analog=True, output='zpk')


def splane_eval(s):
    """
    `s` is a value on the analog S plane.  The frequency response at 10 Hz
    would be s = 1j*2*pi*10, for instance.
    """
    return freqs_zpk(z, p, k, -1j * s)[1]


gs = gridspec.GridSpec(2, 3, width_ratios=[2.5, 1, 1], height_ratios=[2.5, 1])

fig = plt.figure(figsize=(9, 7))

ax_cplot = fig.add_subplot(gs[0, 0])
cplot(splane_eval, re=(-r, r), im=(-r, r), axes=ax_cplot)
ax_cplot.set_xlabel('$\sigma$')
ax_cplot.set_ylabel('$j \omega$')
ax_cplot.axhline(0, color='white', alpha=0.15)
ax_cplot.axvline(0.5, color='white', alpha=0.15)
ax_cplot.set_title('S plane')
ax_cplot.axis('equal')

w, h = freqs_zpk(z, p, k, np.linspace(-r, r, 500))

ax_fr = fig.add_subplot(gs[0, 1], sharey=ax_cplot)
ax_fr.plot(abs(h), w)
ax_fr.invert_xaxis()
ax_fr.tick_params(axis='y', left=False, right=True,
                  labelleft=False,)
ax_fr.set_xlabel('Magnitude')
ax_fr.grid(True, which='both')

ax_ph = fig.add_subplot(gs[0, 2], sharey=ax_cplot)
ax_ph.plot(np.rad2deg(np.angle(h)), w)
ax_ph.invert_xaxis()
ax_ph.tick_params(axis='y', left=False, right=True,
                  labelleft=False, labelright=True)
ax_ph.set_xlabel('Phase [degrees]')
ax_ph.set_ylabel('Frequency [rad/s]')
ax_ph.yaxis.set_label_position("right")
ax_ph.grid(True, which='both')
ax_ph.margins(0.05, 0)

w, h = freqs_zpk(z, p, k, np.linspace(f_c / 10, f_c * 10, 500))

ax_ll = fig.add_subplot(gs[1, 0:])
ax_ll.semilogx(w, 20 * np.log10(abs(h)))
ax_ll.grid(True, which='both')
ax_ll.margins(0, 0.05)
ax_ll.set_xlabel('Frequency [rad/s]')
ax_ll.set_ylabel('Magnitude [dB]')

plt.tight_layout()
