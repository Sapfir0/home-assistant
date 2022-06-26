import colorsys
from Interpolate import Interpolate

def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a) / (n - 1)
    return [diff * i + a for i in range(n)]


def ensure_list(x):
    if isinstance(x, list):
        return x
    return [x]


# если передать яркость, то она будет константной
def rgb_and_brightness(total_time, rgb_sequence, defaultBrightness=None):
    """Return interpolator objects for `rgb` and `brightness`.
    This interpolates in the HSV domain and converts it back to RGB.
    Parameters
    ----------
    total_time : int
        Total time.
    rgb_sequence : list of (r, g, b) tuples
        List with tuples of RGB values, where the values are integers.
    Returns
    -------
    rgb : callable
        Interpolation object that returns RGB values as function of time.
    brightness : callable
        Interpolation object that returns brightness values as function of time.
    """
    xs = linspace(0, total_time, len(rgb_sequence))
    hsvs = zip(*[colorsys.rgb_to_hsv(*rgb) for rgb in rgb_sequence])
    hue, saturation, value = [Interpolate(xs, ys) for ys in hsvs]
    # start at brightness=5 because it considers 1 to be off...
    _brightness = defaultBrightness if defaultBrightness else Interpolate([0, total_time], [5, 255])

    def rgb(t):
        rgb = colorsys.hsv_to_rgb(hue(t), saturation(t), value(t))
        return tuple(round(x) for x in rgb)

    def brightness(t):
        return round(_brightness(t))

    return rgb, brightness
