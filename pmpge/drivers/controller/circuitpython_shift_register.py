# See https://docs.circuitpython.org/en/latest/shared-bindings/keypad/
# noinspection PyUnresolvedReferences
import board
# noinspection PyUnresolvedReferences
import keypad

from pmpge.controller import Controller

values: list[bool] = [False for _ in range(12)]
# This maps the key events to values.
event_map: list[int] = [0 for _ in range(12)]

key_count = 8  # TODO: This needs to be configurable.
# Values: St, Sl, L, R, U, D, A, B, X, Y, LS, RS
# Index:  0,  1,  2, 3, 4, 5, 6, 7, 8, 9, 10, 11
#
# This is the mapping for an EdgeBadge
# Events: B, A, St, Sl, R, D, U, L
# Index:  0, 1, 2,  3,  4, 5, 6, 7
event_map_data: list[int] = [7, 6, 0, 1, 3, 5, 4, 2]  # TODO: This needs to be configurable.
for i, key in enumerate(event_map_data):
    event_map[i] = key

shift_register = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=key_count,
    value_when_pressed=True)


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
        values[event_map[event.key_number]] = event.pressed

    Controller.update(values)


def deinit():
    """
    Simply clear the controller settings and the shift register.
    """
    Controller.reset()
    shift_register.reset()
