"""
Created on Thu Mar 14 2013

Generate lookup tables for 2D lightness/hue colormaps
"""
import numpy as np
import matplotlib.pyplot as plt
from colorspacious import cspace_convert

new_space = "JCh"

# Convert the RGB corners to JCh to know the total possible range
RGB_corners = ((0, 0, 1),
               (0, 1, 0),
               (0, 1, 1),
               (1, 0, 0),
               (1, 0, 1),)

JCh_corners = cspace_convert(RGB_corners, "sRGB1", new_space)
C_max = max(JCh_corners[:, 1])


def dist_to_wall(J, C, h):
    """
    Distance from a point in JCh space to the nearest wall of the RGB cube

    Not a very meaningful number; just used for optimization.  Points inside
    RGB cube are positive; points outside return 0.  (This is not necessarily
    monotonically decreasing.)

    Parameters
    ----------
    J : float
        Lightness from 0 (black) to 100 (white)
    C : float
        Chroma, varies from 0 to 111 within the default RGB cube
    h : float
        Hue angle, which is cyclic from 0 to 360 degrees

    Returns
    -------
    dist : float
        Distance. RGB values vary from 0 to 1, so this varies from 0.5 to 1.

    Examples
    --------
    A point at the center of JCh space will be roughly near the center of RGB
    space, and so should be a distance of around 0.5 from any wall.

    >>> J, C, h = 50, 0, 0
    >>> dist_to_wall(J, C, h)
    0.42313755309145551

    White and black are at corners, so 0 distance from three walls

    >>> J, C, h = 100, 0, 0
    >>> dist_to_wall(J, C, h)
    0
    >>> J, C, h = 0, 0, 0
    >>> dist_to_wall(J, C, h)
    0

    """
    if J == 0 or J == 100:
        return 0

    r, g, b = cspace_convert((J, C, h), new_space, "sRGB1")

    # RGB vary from 0 to 1
    dists = np.array((1-r, 1-g, 1-b, r, g, b)).clip(0, 1)

    # Colorspacious produces NaNs outside of the RGB cube. Convert to zeros
    dists = np.nan_to_num(dists)

    return min(dists)


def find_wall(J, h):
    """
    Finds maximum C value that can be represented in RGB for a given J and h

    Parameters
    ----------
    J : float
        Lightness from 0 (black) to 100 (white)
    h : float
        Hue angle, which is cyclic from 0 to 360 degrees

    Returns
    -------
    C : float
        Chroma, varies from 0 to 111 within the default RGB cube
    """
    if J == 0 or J == 100:
        return 0

    tol = 1/1000
    low = 0.0
    high = C_max + 10
    assert high > low
    assert (high + tol) > high

    def f(C):
        return dist_to_wall(J, C, h)

    # Bisection method from http://stackoverflow.com/a/15961284/125507
    while (high - low) > tol:

        mid = (low + high) / 2
        if f(mid) == 0:
            high = mid
        else:
            low = mid
    return high


if __name__ == '__main__':
    J_lutsize = 1024
    h_lutsize = 1024

    # Lightness includes 0 (black) and 100 (white)
    J_vals = np.linspace(0, 100, J_lutsize, endpoint=True)
    # Hue is cyclic, where 360 degrees = 0 degrees
    h_vals = np.linspace(0, 360, h_lutsize, endpoint=False)

    def create_max_chroma_lut():
        print('Generating max chroma colormap')
        max_chroma_lut = np.ones((J_lutsize, h_lutsize, 3))

        for n, J in enumerate(J_vals):
            print('J =', J)
            for m, h in enumerate(h_vals):
                C = find_wall(J, h)
                if J == 0:
                    rgb = np.zeros(3)
                if J == 100:
                    rgb = np.ones(3)
                else:
                    rgb = cspace_convert((J, C, h), new_space, "sRGB1")
                assert -0.01 <= rgb.min()
                assert rgb.max() <= 1.02
                max_chroma_lut[n, m] = rgb

        return max_chroma_lut.clip(0, 1)

    def create_C_lut():
        print('Generating max chroma lookup table')
        C_lut = np.ones((J_lutsize, h_lutsize))

        # Lightness includes 0 (black) and 100 (white)
        J_vals = np.linspace(0, 100, J_lutsize, endpoint=True)
        # Hue is cyclic, where 360 degrees = 0 degrees (= red??)
        h_vals = np.linspace(0, 360, h_lutsize, endpoint=False)

        for n, J in enumerate(J_vals):
            print('J =', J)
            for m, h in enumerate(h_vals):
                C = find_wall(J, h)
                if J == 0:
                    C = 0
                if J == 100:
                    C = 0
                C_lut[n, m] = C

        return C_lut

    def create_pastel_lut():
        print('Generating constant chroma colormap')
        pastel_chroma_lut = np.ones((J_lutsize, h_lutsize, 3))
        C_lut_1d = C_lut.min(1)

        for n, J in enumerate(J_vals):
            C = C_lut_1d[n]
            print('J =', J, 'C = ', C)
            for m, h in enumerate(h_vals):
                rgb = cspace_convert((J, C, h), new_space, "sRGB1")
                assert -0.01 <= rgb.min()
                assert rgb.max() <= 1.02
                pastel_chroma_lut[n, m] = rgb

        return pastel_chroma_lut

    try:
        max_chroma_lut = np.load('max_chroma_lut.npy')
    except FileNotFoundError:
        max_chroma_lut = create_max_chroma_lut()
        np.save('max_chroma_lut.npy', max_chroma_lut)

    plt.figure('Max chroma')
    plt.imshow(max_chroma_lut.clip(0, 1), origin='lower',
               interpolation='bilinear', extent=(0, 360, 0, 100))
    plt.xlabel('h')
    plt.ylabel('J')
    plt.axis('auto')
    plt.tight_layout()

    try:
        C_lut = np.load('C_lut.npy')
    except FileNotFoundError:
        C_lut = create_C_lut()
        np.save('C_lut.npy', C_lut)

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, num='Maximum C')
    ax1.plot(C_lut.min(1), J_vals, label='min')
    ax1.plot(C_lut.max(1), J_vals, label='max')
    ax1.margins(0)
    ax1.set_xlabel('C')
    ax1.set_ylabel('J')
    ax1.legend()

    ax2.imshow(C_lut, origin='lower', interpolation='bilinear',
               extent=(0, 360, 0, 100))
    ax2.set_xlabel('h')
    ax2.axis('auto')
    plt.tight_layout()

    try:
        pastel_chroma_lut = np.load('pastel_lut.npy')
    except FileNotFoundError:
        pastel_chroma_lut = create_pastel_lut()
        np.save('pastel_lut.npy', pastel_chroma_lut)

    plt.figure('Constant chroma')
    plt.imshow(pastel_chroma_lut.clip(0, 1), origin='lower',
               interpolation='bilinear', extent=(0, 360, 0, 100))
    plt.xlabel('h')
    plt.ylabel('J')
    plt.axis('auto')
    plt.tight_layout()
