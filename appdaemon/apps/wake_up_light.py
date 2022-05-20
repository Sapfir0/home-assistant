"""Emulates a Philips Wake-up Light / sunrise.
This cycles through a sequence of RGB tuples and then
linearily interpolates them in HSV color space as time
proceeds.
The routine can be triggered by toggling an input_boolean.
The sequence is canceled by turning the light on and off.
# Example `apps.yaml` config:
```
wake_up_light:
  module: wake_up_light
  class: WakeUpLight
  total_time: 900
  lamp: "light.bedroom_lamp"
  input_boolean: "input_boolean.wake_up_light"
```
# Example `configuration.yaml`:
```
input_boolean:
  wake_up_light:
    name: Start wake up light
    initial: off
    icon: mdi:weather-sunset-up
```
"""

import bisect
import colorsys

import hassapi as hass

DEFAULT_LAMP = "light.bedroom_lamp"
DEFAULT_TOTAL_TIME = 900
DEFAULT_INPUT_BOOLEAN = "input_boolean.wake_up_light"

DEFAULTS = {
    "lamp": DEFAULT_LAMP,
    "total_time": DEFAULT_TOTAL_TIME,
    "input_boolean": DEFAULT_INPUT_BOOLEAN,
}

RGB_SEQUENCE = [
    (255, 0, 0),
    (255, 0, 0),
    (255, 63, 0),
    (255, 120, 0),
    (255, 187, 131),
    (255, 205, 166),
]

MIN_TIME_STEP = 2  # time between settings


class Interpolate:
    def __init__(self, xs, ys):
        if any(y - x <= 0 for x, y in zip(xs, xs[1:])):
            raise ValueError("xs must be in strictly ascending order!")
        assert len(xs) == len(ys)
        self.xs = xs
        self.ys = ys
        intervals = zip(xs, xs[1:], ys, ys[1:])
        self.slopes = [(y2 - y1) / (x2 - x1) for x1, x2, y1, y2 in intervals]

    def __call__(self, x):
        if not (self.xs[0] <= x <= self.xs[-1]):
            raise ValueError("x out of bounds!")
        if x == self.xs[-1]:
            return self.ys[-1]
        i = bisect.bisect_right(self.xs, x) - 1
        return self.ys[i] + self.slopes[i] * (x - self.xs[i])


def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a) / (n - 1)
    return [diff * i + a for i in range(n)]


def ensure_list(x):
    if isinstance(x, list):
        return x
    return [x]


def rgb_and_brightness(total_time, rgb_sequence):
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
    # start at brightness=2 because it considers 1 to be off...
    _brightness = Interpolate([0, total_time], [5, 255])

    def rgb(t):
        rgb = colorsys.hsv_to_rgb(hue(t), saturation(t), value(t))
        return tuple(round(x) for x in rgb)

    def brightness(t):
        return round(_brightness(t))

    return rgb, brightness


class WakeUpLight(hass.Hass):
    def initialize(self):
        self.input_boolean = self.args.get("input_boolean", DEFAULT_INPUT_BOOLEAN)
        self.listen_state(self.start_cb, self.input_boolean, new="on")
        # cancel when turning off input boolean
        self.listen_state(self.cancel_cb, self.input_boolean, oneshot=True, new="off")

        self.todos = []

    def start_cb(self, entity, attribute, old, new, kwargs):
        self.log(f"start_cb, kwargs: {kwargs}")
        self.set_state(self.input_boolean, state="off")
        self.start()

    def maybe_defaults(self, kwargs):
        for key in set(DEFAULTS) | set(self.args):
            if key in kwargs:
                continue
            elif key in self.args:
                kwargs[key] = self.args[key]
            else:
                kwargs[key] = DEFAULTS[key]

    @property
    def done_signal(self):
        return f"{self.input_boolean}.done"

    def start(self, **kwargs):
        self.maybe_defaults(kwargs)
        total_time = kwargs["total_time"]
        lamp = kwargs["lamp"]
        rgb, brightness = rgb_and_brightness(total_time, RGB_SEQUENCE)
        steps = min(total_time // MIN_TIME_STEP, 255) + 1
        for t in linspace(0, total_time, steps):
            service_kwargs = {
                "entity_id": lamp,
                "rgb_color": rgb(t),
                "brightness": brightness(t),
                "transition": total_time / (steps - 1),
            }
            is_done = t == total_time
            todo = self.run_in(
                self.set_state_cb,
                t,
                service_kwargs=service_kwargs,
                is_done=is_done,
                **kwargs,
            )
            self.todos.append(todo)

        # Cancel when turning the light off.
        for l in ensure_list(lamp):
            self.listen_state(
                self.cancel_cb, l, oneshot=True, new="off", timeout=total_time
            )


    def set_state_cb(self, kwargs):
        service_kwargs = kwargs.pop("service_kwargs")
        self.log(f"Setting light: {service_kwargs}")
        self.call_service("light/turn_on", **service_kwargs)
        if kwargs.pop("is_done"):
            self.fire_event(self.done_signal, **kwargs)
            self.log(self.done_signal)

    def cancel_cb(self, entity, attribute, old, new, kwargs):
        assert new == "off"
        self.log(f"Canceling sequence, old: {old}, new: {new}")
        while self.todos:
            self.cancel_timer(self.todos.pop())