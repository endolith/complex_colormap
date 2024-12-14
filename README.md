# complex_colormap

Plot complex functions in perceptually-uniform color space

This generates a bivariate color map that adjusts both lightness and hue, for
plotting complex functions, the magnitude and phase of signals, etc.

Magnitude is mapped to lightness and phase angle is mapped to hue in a
perceptually-uniform color space (previously
[LCh](https://en.wikipedia.org/wiki/CIELAB_color_space#Cylindrical_model),
now
[CIECAM02's JCh](https://en.wikipedia.org/wiki/CIECAM02#Appearance_correlates)).

## Usage

Since [matplotlib doesn't handle 2D colormaps natively](https://github.com/matplotlib/matplotlib/issues/14168), it's currently implemented
as a `cplot` function that adds to an `axes` object, which you can then apply
further MPL features to:

```py
ax_cplot = fig.add_subplot()
cplot(splane_eval, re=(-r, r), im=(-r, r), axes=ax_cplot)
ax_cplot.set_xlabel('$\sigma$')
ax_cplot.axis('equal')
…
```

See [the example script](/examples/analog_filter.py).

## Color mapping

There are currently two ways to handle the chroma information:

### Constant chroma (`'const'`)

For each lightness `J`, find the maximum chroma that can be represented in RGB
for *any* hue, and then use that for every *other* hue. This produces images with
perceptually accurate magnitude variation, but the colors are muted and more
difficult to perceive.

[![constant chroma colormap](https://live.staticflickr.com/4646/39058425412_67d203f0b8.jpg)](https://flic.kr/p/22vsD6N)

![f(z) = z](https://c1.staticflickr.com/5/4682/39058425052_ff82772542_o.png)
![f(z) = sin(z)](https://c1.staticflickr.com/5/4575/39058424492_3210b35fe6_o.png)

### Maximum chroma (`'max'`)

For each lightness `J` and hue `h`, find the maximum chroma that can be
represented in RGB.  This produces vivid images, but the chroma variation
produces misleading streaks as it makes sharp angles around the RGB edges.

[![maximum chroma colormap](https://live.staticflickr.com/4599/39058425252_0ea7a3f62a.jpg)](https://flic.kr/p/22vsD43)

![f(z) = z](https://c1.staticflickr.com/5/4689/39058424882_bc4d9148a9_o.png)
![f(z) = sin(z)](https://c1.staticflickr.com/5/4565/39058424742_8d33ea9f38_o.png)

## Example

[analog_filter.py](/examples/analog_filter.py) uses a constant-chroma map to
visualize the poles and zeros of an analog bandpass filter,
with accompanying magnitude and phase plots along jω axis, and a log-dB plot of
magnitude for comparison:

[![bandpass filter](https://c1.staticflickr.com/5/4743/39109387514_b78745ecf2_z.jpg)](https://flic.kr/p/22zXQmJ)

## Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:

    ```shell
    make publish
    ```

## License

complex_colormap is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
