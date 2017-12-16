# complex_colormap
Plot complex functions in perceptually-uniform colorspace

This generates a bivariate colormap that adjusts both lightness 
and hue, for plotting complex functions, the magnitude and
phase of signals, etc.

Magnitude is mapped to lightness and phase angle is mapped to hue
in a perceptually-uniform colorspace (previously
[LCh](https://en.wikipedia.org/wiki/Lab_color_space#Cylindrical_representation:_CIELCh_or_CIEHLC), 
now [CIECAM02's JCh](https://en.wikipedia.org/wiki/CIECAM02#Appearance_correlates))

There are currently two ways to handle the chroma information:
- `'max'`: For each lightness `J` and hue `h`, find the maximum
    chroma that can be represented in RGB.  This produces vivid 
    images, but the chroma variation produces misleading streaks.
- `'const'`: For each lightness `J`, find the maximum
    chroma that can be represented in RGB for *any* hue, and then 
    use that for every other hue. This produces images with 
    accurate magnitude variation, but the colors are muted and
    more difficult to perceive.
