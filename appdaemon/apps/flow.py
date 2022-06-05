# import hassapi as hass
# from lib.RGB import linspace, ensure_list
# from lib.Interpolate import Interpolate
# import colorsys

# DEFAULT_LAMP = "light.bedroom_lamp"
# DEFAULT_TOTAL_TIME = 100
# DEFAULT_INPUT_BOOLEAN = "input_boolean.flow"

# DEFAULTS = {
#     "lamp": DEFAULT_LAMP,
#     "input_boolean": DEFAULT_INPUT_BOOLEAN,
#     "brightness": 100,
#     "gradient": 'megatron'
# }



# COLORS = {
#     'megatron': [(198,255,221),(251, 215, 134), (247, 121, 125) ], #https://uigradients.com/#MegaTron
#     'red_sunset': [(53, 92, 125), (108, 91, 123), (192, 108, 132)], #https://uigradients.com/#RedSunset
#     'sunrise': [
#         (0, 255, 100),
#         (250, 105, 0),
#         (250, 40, 0),
#         (255, 0, 0),
#         (10, 10, 255),
#         (255, 0, 100),
#         (200, 0, 255),
#         (0, 255, 0),
#         (255, 255, 255),
#     ],
# }
# MIN_TIME_STEP = 2  # time between settings

# def get_rgb(rgb_sequence):
#     xs = linspace(0, DEFAULT_TOTAL_TIME, len(rgb_sequence))
#     hsvs = zip(*[colorsys.rgb_to_hsv(*rgb) for rgb in rgb_sequence])
#     hue, saturation, value = [Interpolate(xs, ys) for ys in hsvs]

#     def rgb(t):
#         rgb = colorsys.hsv_to_rgb(hue(t), saturation(t), value(t))
#         return tuple(round(x) for x in rgb)

#     return rgb


# class Flow(hass.Hass):

#     def initialize(self):
#         self.input_boolean = self.args.get("input_boolean", DEFAULT_INPUT_BOOLEAN)
#         self.listen_state(self.start_cb, self.input_boolean, new="on")

#     def start_cb(self, entity, attribute, old, new, kwargs):
#         self.log(f"start_cb, kwargs: {kwargs}")
#         self.set_state(self.input_boolean, state="off")
#         self.start()

#     def maybe_defaults(self, kwargs):
#         for key in set(DEFAULTS) | set(self.args):
#             if key in kwargs:
#                 continue
#             elif key in self.args:
#                 kwargs[key] = self.args[key]
#             else:
#                 kwargs[key] = DEFAULTS[key]

#     @property
#     def done_signal(self):
#         return f"{self.input_boolean}.done"


#     def start(self, **kwargs):
#         self.maybe_defaults(kwargs)
#         self.brightness = kwargs["brightness"]
#         self.lamp = kwargs["lamp"]
#         self.gradient = COLORS[kwargs["gradient"]]
        
#         self.steps = min(DEFAULT_TOTAL_TIME // MIN_TIME_STEP, 255) + 1
#         self.iterateForward(self.gradient)
        
#     def iterateForward(self, gradient, **kwargs):
#         rgb = get_rgb(gradient)
#         for t in linspace(0, DEFAULT_TOTAL_TIME, self.steps):
#             currentRgb = rgb(t)
#             service_kwargs = {
#                 "entity_id": self.lamp,
#                 "rgb_color": currentRgb,
#                 "brightness": self.brightness,
#                 "transition": 20,
#              }
#             # print(DEFAULT_TOTAL_TIME, self.steps - 1, service_kwargs["transition"])
#             self.log(f"Setting light: {service_kwargs}")
#             # self.call_service("light/turn_on", **service_kwargs)

#             # Cancel when turning the light off.
#             for l in ensure_list(self.lamp):
#                 self.listen_state(
#                     self.cancel_cb, l, oneshot=True, new="off"
#                 )

#             if (currentRgb == gradient[-1]):
#                 self.log("We are at the end, going backward")
#                 gradient.reverse()
#                 # self.iterateForward(gradient)


#     def cancel_cb(self, entity, attribute, old, new, kwargs):
#         assert new == "off"
#         self.log(f"Canceling sequence, old: {old}, new: {new}")
#         while self.todos:
#             self.cancel_timer(self.todos.pop())