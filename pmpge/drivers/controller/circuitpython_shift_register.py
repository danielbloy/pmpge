#
# This controller driver is designed to work on devices that use a shift
# register to access the controller pins such as on a PyBadge or EdgeBadge.
#
# It is a fairly lightweight driver and only requires minimal configuration
# to be provided so the shift register can be accessed and the resultant
# values can be mapped back to the Controller buttons. The Controller needs
# the button values to be provided in the following order:
#
# Index: 0,     1,      2, 3, 4, 5, 6, 7, 8, 9, 10, 11
# Value: Start, Select, L, R, U, D, A, B, X, Y, LS, RS
#
# Therefore, the configuration data needs to map the order that the values
# come out of the shift register to the controller values. On an EdgeBadge
# the values come out in the following order (note the EdgeBadge only has
# 8 buttons):
#
# Index:  0, 1, 2,     3,       4, 5, 6, 7
# Button: B, A, Start, Slelect, R, D, U, L
#
# Therefore, the mapping for an EdgeBadge is:
#
# [7, 6, 0, 1, 3, 5, 4, 2]
#
# The following configuration values are required to use this driver (with
# example values for an EdgeBadge):
#
# import board
# BUTTON_CLOCK = board.BUTTON_CLOCK
# BUTTON_OUT = board.BUTTON_OUT
# BUTTON_LATCH = board.BUTTON_LATCH
# BUTTON_MAPPING = [7, 6, 0, 1, 3, 5, 4, 2]
#
# REFERENCES
#
# See https://docs.circuitpython.org/en/latest/shared-bindings/keypad/
#
# noinspection PyUnresolvedReferences
from keypad import ShiftRegisterKeys

from pmpge.controller import Controller

values: list[bool] = [False for _ in range(12)]
button_map: list[int] = [0 for _ in range(12)]
shift_register: ShiftRegisterKeys = None


# noinspection PyUnresolvedReferences
def setup():
    """
    Sets up the shift register.
    """
    global shift_register
    from pmpge.environment import config

    for i, key in enumerate(config.BUTTON_MAPPING):
        button_map[i] = key

    shift_register = ShiftRegisterKeys(
        clock=config.BUTTON_CLOCK,
        data=config.BUTTON_OUT,
        latch=config.BUTTON_LATCH,
        key_count=len(config.BUTTON_MAPPING),
        value_when_pressed=True)


setup()


def init(_):
    """
    Simply clear the controller settings and the shift register.
    """
    Controller.reset()
    shift_register.reset()


def update(df: float):
    while True:
        event = shift_register.events.get()
        if event is None:
            break

        # noinspection PyTypeChecker
        values[button_map[event.key_number]] = event.pressed

    Controller.update(values)


def deinit():
    """
    Simply clear the controller settings and the shift register.
    """
    Controller.reset()
    shift_register.reset()
