# complex_colormap
Plot complex functions in perceptually-uniform colorspace

This generates a bivariate colormap that adjusts both lightness and hue, for plotting complex functions, the magnitude and phase of signals, etc.

Magnitude is mapped to lightness and phase angle is mapped to hue in a perceptually-uniform colorspace (previously [LCh](https://en.wikipedia.org/wiki/Lab_color_space#Cylindrical_representation:_CIELCh_or_CIEHLC), now [CIECAM02's JCh](https://en.wikipedia.org/wiki/CIECAM02#Appearance_correlates)).

There are currently two ways to handle the chroma information:
- `'max'`: For each lightness `J` and hue `h`, find the maximum chroma that can be represented in RGB.  This produces vivid images, but the chroma variation produces misleading streaks.
- `'const'`: For each lightness `J`, find the maximum chroma that can be represented in RGB for *any* hue, and then use that for every other hue. This produces images with accurate magnitude variation, but the colors are muted and more difficult to perceive.

## Constant chroma

[![constant chroma colormap](https://c1.staticflickr.com/5/4646/39058425412_0e83cf740f_n.jpg)](https://flic.kr/p/22vsD6N)
![f(z) = z](https://c1.staticflickr.com/5/4682/39058425052_ff82772542_o.png)
![f(z) = sin(z)](https://c1.staticflickr.com/5/4575/39058424492_3210b35fe6_o.png)

## Maximum chroma

[![maximum chroma colormap](https://c1.staticflickr.com/5/4599/39058425252_ae2c812dd9_n.jpg)](https://flic.kr/p/22vsD43)
![f(z) = z](https://c1.staticflickr.com/5/4689/39058424882_bc4d9148a9_o.png)
![f(z) = sin(z)](https://c1.staticflickr.com/5/4565/39058424742_8d33ea9f38_o.png)

