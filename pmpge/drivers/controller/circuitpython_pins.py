#
# This controller driver is designed to work on devices where the buttons are
# connected directly to pins. It is about as lightweight a driver as can be.
# It does require that each button to be used is specified in configuration.
# The configuration properties are the same as the Controller constants.
#
#   CONTROLLER_START = <pin>
#   CONTROLLER_SELECT = <pin>
#   CONTROLLER_LEFT = SW_LEFT
#   CONTROLLER_RIGHT = SW_RIGHT
#   CONTROLLER_UP = SW_UP
#   CONTROLLER_DOWN = SW_DOWN
#   CONTROLLER_A = SW_A
#   CONTROLLER_B = SW_B
#   CONTROLLER_X = SW_X
#   CONTROLLER_Y = SW_Y
#   CONTROLLER_LS = <pin>
#   CONTROLLER_RS = <pin>
#
# LIMITATION
#
# This driver has only been tested on the Pimoroni PicoSystem which uses
# pullup resistors.
#
# REFERENCES
#
# See https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing
#
# noinspection PyUnresolvedReferences
from adafruit_debouncer import Debouncer
# noinspection PyUnresolvedReferences
from digitalio import DigitalInOut, Direction, Pull

from pmpge.controller import Controller

values: list[bool] = [False for _ in range(12)]
pins: list[DigitalInOut] = [None for _ in range(12)]
buttons: list[Debouncer] = [None for _ in range(12)]
pullup: bool = True


def create_pin(pin, pullup: bool):
    """
    Simple Pin using a boolean value for input logic level on a Pin.

    :param pin:    The pin to use as an input pin.
    :param pullup: Whether the pin should be pulled up or not.
    """
    result = DigitalInOut(pin)
    result.direction = Direction.INPUT

    if pullup:
        result.pull = Pull.UP
    else:
        result.pull = Pull.DOWN

    return result


def create_pins():
    """
    Creates the pins used for the controller buttons.

    # FUTURE: Add support for specifying active-high pins (i.e. pulldown = False).
    """
    from pmpge.environment import config
    global pullup

    if hasattr(config, 'CONTROLLER_PULLUP'):
        pullup = config.CONTROLLER_PULLUP

    if hasattr(config, 'CONTROLLER_START'):
        pins[Controller.BUTTON_START] = create_pin(config.CONTROLLER_START, pullup)

    if hasattr(config, 'CONTROLLER_SELECT'):
        pins[Controller.BUTTON_SELECT] = create_pin(config.CONTROLLER_SELECT, pullup)

    if hasattr(config, 'CONTROLLER_LEFT'):
        pins[Controller.BUTTON_LEFT] = create_pin(config.CONTROLLER_LEFT, pullup)

    if hasattr(config, 'CONTROLLER_RIGHT'):
        pins[Controller.BUTTON_RIGHT] = create_pin(config.CONTROLLER_RIGHT, pullup)

    if hasattr(config, 'CONTROLLER_UP'):
        pins[Controller.BUTTON_UP] = create_pin(config.CONTROLLER_UP, pullup)

    if hasattr(config, 'CONTROLLER_DOWN'):
        pins[Controller.BUTTON_DOWN] = create_pin(config.CONTROLLER_DOWN, pullup)

    if hasattr(config, 'CONTROLLER_A'):
        pins[Controller.BUTTON_A] = create_pin(config.CONTROLLER_A, pullup)

    if hasattr(config, 'CONTROLLER_B'):
        pins[Controller.BUTTON_B] = create_pin(config.CONTROLLER_B, pullup)

    if hasattr(config, 'CONTROLLER_X'):
        pins[Controller.BUTTON_X] = create_pin(config.CONTROLLER_X, pullup)

    if hasattr(config, 'CONTROLLER_Y'):
        pins[Controller.BUTTON_Y] = create_pin(config.CONTROLLER_Y, pullup)

    if hasattr(config, 'CONTROLLER_LS'):
        pins[Controller.BUTTON_LS] = create_pin(config.CONTROLLER_LS, pullup)

    if hasattr(config, 'CONTROLLER_RS'):
        pins[Controller.BUTTON_RS] = create_pin(config.CONTROLLER_RS, pullup)


create_pins()

for i, pin in enumerate(pins):
    if pin is not None:
        buttons[i] = Debouncer(pin)


def init(_):
    """
    Simply clear the controller settings.
    """
    for i, v in enumerate(values):
        values[i] = False
    Controller.reset()


def update(df: float):
    for i, button in enumerate(buttons):
        if button is not None:
            button.update()
            values[i] = button.value ^ pullup

    Controller.update(values)


def deinit():
    """
    Simply clear the controller settings.
    """
    for i, v in enumerate(values):
        values[i] = False
    Controller.reset()
