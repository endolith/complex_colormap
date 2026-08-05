import numpy as np
import pytest

from complex_colormap.cplot import const_chroma_colormap, max_chroma_colormap


@pytest.mark.parametrize("func,expected", [
    (const_chroma_colormap,
     [[1.0, 1.0, 1.0],
      [0.0, 0.0, 0.0],
      [0.824, 0.706, 0.314],
      [0.502, 0.502, 0.502]]),
    (max_chroma_colormap,
     [[1.0, 1.0, 1.0],
      [0.051, 0.0, 0.001],
      [0.863, 0.694, 0.0],
      [0.502, 0.502, 0.502]]),
])
def test_colormap_docstring_examples(func, expected):
    z = np.array([[np.inf, 0, 10j, np.nan]])
    result = func(z)
    np.testing.assert_allclose(result[0], expected, atol=1e-3)


@pytest.mark.parametrize("func", [const_chroma_colormap, max_chroma_colormap])
def test_colormap_shape_and_bounds(func):
    z = np.random.randn(10, 12) + 1j * np.random.randn(10, 12)
    result = func(z)
    assert result.shape == (10, 12, 3)
    assert result.min() >= 0.0
    assert result.max() <= 1.0

