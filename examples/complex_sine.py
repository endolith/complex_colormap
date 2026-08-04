# -*- coding: utf-8 -*-
"""Cisoid at varying frequencies, with and without linear amplitude modulation."""
import numpy as np
import matplotlib.pyplot as plt
from complex_colormap.cplot import const_chroma_colormap, max_chroma_colormap

#%% Helpers ------------------------------------------------------------------
def gen_x(N, f, AM):
    t = np.arange(N)/N
    xbase = np.cos(2*np.pi*f*t) + 1j*np.sin(2*np.pi*f*t)
    x = np.repeat(xbase[None], N, 0)
    if AM:
        x *= t[::-1]
    return x

def imshow(s, alpha=None, cmap=None, aspect='auto',
           interpolation='nearest', title=None, **kw):
    fig = plt.figure()
    ax = plt.gca()
    ax.imshow(s, cmap=cmap, alpha=alpha, aspect=aspect,
              interpolation=interpolation, **kw)
    _ = [getattr(ax, 'set_%s' % s)([]) for s in
         ('xticks', 'yticks', 'xticklabels', 'yticklabels')]
    if title:
        ax.set_title(title, loc='left', weight='bold', fontsize=24)
    plt.show()

cms = {'max': max_chroma_colormap,
       'const': const_chroma_colormap}

#%% Configure (sandbox) ------------------------------------------------------
# interactive example

# colormap mode
mode = ('max', 'const')[0]
# sine length
N = 512
# sine frequency
f = 2
# whether to use amplitude modulation
AM = 0

# Execute --------------------------------------------------------------------
cm = cms[mode]
x = gen_x(N, f, AM)
s = cm(x)
imshow(s)

#%% Run example --------------------------------------------------------------
N = 512
for mode in ('const', 'max'):
    for f in (1, 2):
        for AM in (0, 1):
            title = 'cisoid: f={}{} | {}_chroma'.format(
                f, ', AM' if AM else '', mode)
            cm = cms[mode]
            x = gen_x(N, f, AM)
            s = cm(x)
            imshow(s, title=title)
