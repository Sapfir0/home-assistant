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

from lib.RGB import linspace, rgb_and_brightness, ensure_list
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


class WakeUpLight(hass.Hass):
    def initialize(self):
        self.input_boolean = self.args.get("input_boolean", DEFAULT_INPUT_BOOLEAN)
        self.listen_state(self.start_cb, self.input_boolean, new="on")
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