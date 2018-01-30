"""
Created on Thu Mar 14 2013

Use lookup tables to color pictures

TODO: Allow the infinity squashing function to be customized
TODO: Colorspacious doesn't quite reach white for J = 100?
TODO: cplot(np.tan, re=(3, 3), im=(-3, 3)) division by zero
TODO: Lookup table is 8 MiB!
TODO: Make phase rotatable?
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image
from scipy.interpolate import interp1d, RectBivariateSpline
from matplotlib.colors import colorConverter
from colorspacious import cspace_convert
import numbers
import os

new_space = "JCh"

# 2D C vs (J, h)
C_lut = np.load(os.path.join(os.path.dirname(__file__), 'C_lut.npy'))

# TODO: -360 to +360 is overkill for -180 to +180, just need a little extra
max_J_vals = np.linspace(0, 100, C_lut.shape[0], endpoint=True)
max_h_vals = np.linspace(-360, 0, C_lut.shape[1], endpoint=False)
max_h_vals = np.concatenate((max_h_vals, max_h_vals + 360))
max_interpolator = RectBivariateSpline(max_J_vals, max_h_vals,
                                       np.tile(C_lut, 2))

# 1D C vs J
C_lut_1d = C_lut.min(1)

const_J_vals = np.linspace(0, 100, len(C_lut_1d), endpoint=True)
const_interpolator = interp1d(const_J_vals, C_lut_1d, kind='linear')


def to_rgb(color):
    if isinstance(color, numbers.Number):
        return colorConverter.to_rgb(str(color))
    else:
        return colorConverter.to_rgb(color)


def const_chroma_colormap(z, nancolor='gray'):
    """
    Map complex value to color, with constant chroma at each lightness

    Magnitude is represented by lightness and angle is represented by hue.
    The interval [0, ∞) is mapped to lightness [0, 100].

    Parameters
    ----------
    z : array_like
        Complex numbers to be mapped.
    nancolor
        Color used to represent NaNs.  Can be any valid matplotlib color,
        such as ``'k'``, ``'deeppink'``, ``'0.5'`` [gray],
        ``(1.0, 0.5, 0.0)`` [orange], etc.

    Returns
    -------
    rgb : ndarray
        Array of colors, with values varying from 0 to 1.  Shape is same as
        input, but with an extra dimension for R, G, and B.

    Examples
    --------
    A point with infinite magnitude will map to white, magnitude 0 will map to
    black, and a point with magnitude 10 and phase of π/2 will map to a
    pale yellow.  NaNs will map to gray by default (which is not produced
    otherwise):

    >>> const_chroma_colormap([[np.inf, 0, 10j, np.nan]])
    array([[[ 1.   ,  1.   ,  1.   ],
            [ 0.   ,  0.   ,  0.   ],
            [ 0.824,  0.706,  0.314],
            [ 0.502,  0.502,  0.502]]])
    """
    # Input magnitude is 0 to inf and phase 0 to 2pi

    # J is from 0 to 100
    # TODO: Somewhere between 98.24 and 98.34, the min C drops close to 0, so
    # cut it off before 100?  Instead of having multiple J values that map to
    # white.  No such problem at black end.  Probably varies with illuminant?
    J = (1.0 - (1 / (1.0 + np.abs(z)**0.3))) * 100

    # h is from 0 to 360 degrees
    h = np.angle(z, deg=True)

    C = const_interpolator(J)

    # So if z is (vertical, horizontal)
    # imshow expects shape of (vertical, horizontal, 3)
    JCh = np.stack((J, C, h), axis=-1)

    rgb = cspace_convert(JCh, new_space, "sRGB1")

    # White for infinity (colorspacious doesn't quite reach it for J = 100)
    rgb[np.isinf(z)] = (1.0, 1.0, 1.0)

    # Color NaNs
    rgb[np.isnan(z)] = to_rgb(nancolor)

    return rgb.clip(0, 1)


def max_chroma_colormap(z, nancolor='gray'):
    """
    Map complex value to color, with maximum chroma at each lightness

    Magnitude is represented by lightness and angle is represented by hue.
    The interval [0, ∞) is mapped to lightness [0, 100].

    Parameters
    ----------
    z : array_like
        Complex numbers to be mapped.
    nancolor
        Color used to represent NaNs.  Can be any valid matplotlib color,
        such as ``'k'``, ``'deeppink'``, ``'0.5'`` [gray],
        ``(1.0, 0.5, 0.0)`` [orange], etc.

    Returns
    -------
    rgb : ndarray
        Array of colors, with values varying from 0 to 1.  Shape is same as
        input, but with an extra dimension for R, G, and B.

    Examples
    --------
    A point with infinite magnitude will map to white, magnitude 0 will map to
    black, and a point with magnitude 10 and phase of π/2 will map to a
    saturated yellow.  NaNs will map to gray by default (which is not produced
    otherwise):

    >>> max_chroma_colormap([[np.inf, 0, 10j, np.nan]])
    array([[[ 1.   ,  1.   ,  1.   ],
            [ 0.051,  0.   ,  0.001],
            [ 0.863,  0.694,  0.   ],
            [ 0.502,  0.502,  0.502]]])
    """
    # Input magnitude is 0 to inf and phase 0 to 2pi

    # J is from 0 to 100
    J = (1.0 - (1 / (1.0 + np.abs(z)**0.3))) * 100

    # h is from 0 to 360 degrees
    h = np.angle(z, deg=True)

    # TODO: Don't interpolate NaNs and get warnings

    # 2D interpolation of C lookup table
    C = max_interpolator(J, h, grid=False)

    # So if z is (vertical, horizontal)
    # imshow expects shape of (vertical, horizontal, 3)
    JCh = np.stack((J, C, h), axis=-1)

    # TODO: Don't convert NaNs and get warnings

    rgb = cspace_convert(JCh, new_space, "sRGB1")

    # White for infinity (colorspacious doesn't quite reach it for J = 100)
    rgb[np.isinf(z)] = (1.0, 1.0, 1.0)

    # Color NaNs
    rgb[np.isnan(z)] = to_rgb(nancolor)

    return rgb.clip(0, 1)


def cplot(f, re=(-5, 5), im=(-5, 5), points=160000, color='const', file=None,
          dpi=None, axes=None):
    r"""
    Plot a complex function using lightness for magnitude and hue for phase

    Plots the given complex-valued function `f` over a rectangular part
    of the complex plane specified by the pairs of intervals `re` and `im`.

    Parameters
    ----------
    f : callable
        Function to be evaluated
    re : sequence of float
        Range for real axis (horizontal)
    im : sequence of float
        Range for imaginary axis (vertical)
    points : int
        Total number of points in the image. (e.g. points=9 produces a 3x3
        image)
    color : {'max', 'const', callable}
        Which colormap to use.
        If ``'max'``, maximize chroma for each point, which produces vivid
        images with misleading lightness.
        If ``'const'``, then the chroma is held constant for a given lightness,
        producing images with accurate amplitude, but muted colors.
        A custom function can also be supplied.  See Notes.
    file : string or None
        Filename to save the figure to.  If None, figure is displayed on
        screen.
    dpi : [ None | scalar > 0 | ‘figure’]
        The resolution in dots per inch for the saved file. If None it will
        default to the value savefig.dpi in the matplotlibrc file. If
        ‘figure’, it will set the dpi to be the value of the figure.
    axes : matplotlib.axes._subplots.AxesSubplot
        An existing axes object in which to place the plot.

    Returns
    -------
    axes : matplotlib.axes._subplots.AxesSubplot
        Axes object of the plot

    Notes
    -----
    By default, the complex argument (phase) is shown as color (hue) and
    the magnitude is show as lightness. You can also supply a custom color
    function (`color`). This function should take an ndarray of complex
    numbers of shape (n, m) as input and return an ndarray of RGB 3-tuples of
    shape (n, m, 3), containing floats in the range 0.0-1.0.

    Examples
    --------
    Show the default color mapping using the identity function:

    >>> cplot(lambda z: z)
    >>> plt.title(r'$f(z) = e^z$')

    Show the max chroma color mapping:

    >>> cplot(lambda z: z, color='max')
    >>> plt.title(r'$f(z) = e^z$')

    Plot the sine function.  Zeros are black dots, positive real values are
    red, and negative real values are green:

    >>> cplot(np.sin)
    >>> plt.title(r'$f(z) = \sin(z)$')

    Plot the tan function with a smaller range. Poles (infinity) are shown as
    white dots:

    >>> cplot(np.tan, re=(-4, 4), im=(-4, 4))
    >>> plt.title(r'$f(z) = \tan(z)$')

    Plot a function with NaN values as gray:

    >>> func = lambda z: np.sqrt(16 - z.real**2 - z.imag**2)
    >>> cplot(func)
    >>> plt.title(r'$f(z) = \sqrt{16 - ℜ(z)^2 - ℑ(z)^2}$')

    or customize the NaN color by using a custom color function:

    >>> nancolor = 'xkcd:radioactive green'
    >>> color_func = lambda z: const_chroma_colormap(z, nancolor=nancolor)
    >>> cplot(func, color=color_func)
    >>> plt.title(r'$f(z) = \sqrt{16 - ℜ(z)^2 - ℑ(z)^2}$')
    """
    # Modified from mpmath.cplot
    if color == 'const':
        color = const_chroma_colormap
    elif color == 'max':
        color = max_chroma_colormap

    if file:
        axes = None

    fig = None
    if not axes:
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)

    re_lo, re_hi = re
    im_lo, im_hi = im
    re_d = re_hi - re_lo
    im_d = im_hi - im_lo
    M = int(np.sqrt(points * re_d / im_d) + 1)  # TODO: off by one!
    N = int(np.sqrt(points * im_d / re_d) + 1)
    x = np.linspace(re_lo, re_hi, M)
    y = np.linspace(im_lo, im_hi, N)

    # Note: we have to be careful to get the right rotation.
    # Test with these plots:
    #    cplot(np.vectorize(lambda z: z if z.real < 0 else 0))
    #    cplot(np.vectorize(lambda z: z if z.imag < 0 else 0))
    z = x[None, :] + 1j * y[:, None]
    w = color(f(z))

    if type(axes) == matplotlib.image.AxesImage:
        axes.set_data(w)
        axes = axes.axes
    else:
        axes.imshow(w, extent=(re_lo, re_hi, im_lo, im_hi), origin='lower')
        axes.set_xlabel('$\operatorname{Re}(z)$')
        axes.set_ylabel('$\operatorname{Im}(z)$')
    if fig:
        if file:
            plt.savefig(file, dpi=dpi)
        else:
            plt.show()

    return axes


if __name__ == '__main__':
    cplot(lambda z: z, color='max')
    plt.title('$f(z) = z$')

    cplot(lambda z: z, color='const')
    plt.title('$f(z) = z$')
