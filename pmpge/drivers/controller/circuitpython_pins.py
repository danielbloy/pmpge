#
# This controller driver is designed to work on devices where the buttons are
# connected directly to pins. It is about as lightweight a driver as can be.
# It does require that each button to be used is specified in configuration.
# The configuration properties are the same as the Controller constants.
#
#   BUTTON_START = <pin>
#   BUTTON_SELECT = <pin>
#   BUTTON_LEFT = <pin>
#   BUTTON_RIGHT = <pin>
#   BUTTON_UP = <pin>
#   BUTTON_DOWN = <pin>
#   BUTTON_A = <pin>
#   BUTTON_B = <pin>
#   BUTTON_X = <pin>
#   BUTTON_Y = <pin>
#   BUTTON_LS = <pin>
#   BUTTON_RS = <pin>
#
# LIMITATION
#
# This driver has not yet been tested on a device.
#
# REFERENCES
#
# See https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing
#
# noinspection PyUnresolvedReferences
import digitalio
# noinspection PyUnresolvedReferences
from adafruit_debouncer import Debouncer

from pmpge.controller import Controller

values: list[bool] = [False for _ in range(12)]
pins = [None for _ in range(12)]
buttons = [None for _ in range(12)]


def create_pin(pin, pullup: bool = True):
    """
    Simple Pin using a boolean value for input logic level on a Pin.

    :param pin:    The pin to use as an input pin.
    :param pullup: Whether the pin should be pulled up or not.
    """
    result = digitalio.DigitalInOut(pin)
    result.direction = digitalio.Direction.INPUT

    if pullup:
        result.pull = digitalio.Pull.UP
    else:
        result.pull = digitalio.Pull.DOWN

    return result


def create_pins():
    """
    Creates the pins used for the controller buttons.

    # FUTURE: Add support for specifying active-high pins (i.e. pulldown = False).
    """
    from pmpge.environment import config

    if hasattr(config, 'BUTTON_START'):
        pins[Controller.BUTTON_START] = create_pin(config.BUTTON_START)

    if hasattr(config, 'BUTTON_SELECT'):
        pins[Controller.BUTTON_SELECT] = create_pin(config.BUTTON_SELECT)

    if hasattr(config, 'BUTTON_LEFT'):
        pins[Controller.BUTTON_LEFT] = create_pin(config.BUTTON_LEFT)

    if hasattr(config, 'BUTTON_RIGHT'):
        pins[Controller.BUTTON_RIGHT] = create_pin(config.BUTTON_RIGHT)

    if hasattr(config, 'BUTTON_UP'):
        pins[Controller.BUTTON_UP] = create_pin(config.BUTTON_UP)

    if hasattr(config, 'BUTTON_DOWN'):
        pins[Controller.BUTTON_DOWN] = create_pin(config.BUTTON_DOWN)

    if hasattr(config, 'BUTTON_A'):
        pins[Controller.BUTTON_A] = create_pin(config.BUTTON_A)

    if hasattr(config, 'BUTTON_B'):
        pins[Controller.BUTTON_B] = create_pin(config.BUTTON_B)

    if hasattr(config, 'BUTTON_X'):
        pins[Controller.BUTTON_X] = create_pin(config.BUTTON_X)

    if hasattr(config, 'BUTTON_Y'):
        pins[Controller.BUTTON_Y] = create_pin(config.BUTTON_Y)

    if hasattr(config, 'BUTTON_LS'):
        pins[Controller.BUTTON_LS] = create_pin(config.BUTTON_LS)

    if hasattr(config, 'BUTTON_RS'):
        pins[Controller.BUTTON_RS] = create_pin(config.BUTTON_RS)


create_pins()

for i, pin in enumerate(pins):
    if pin is not None:
        buttons[i] = Debouncer(pin)


def init(_):
    """
    Simply clear the controller settings.
    """
    Controller.reset()


def update(df: float):
    for i, button in enumerate(buttons):
        if button is not None:
            button.update()
            values[i] = button.value

    Controller.update(values)


def deinit():
    """
    Simply clear the controller settings.
    """
    Controller.reset()
