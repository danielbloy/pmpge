# See https://docs.circuitpython.org/en/latest/shared-bindings/keypad/
import board
import keypad

from pmpge.controller import Controller

values: list[bool] = [False for _ in range(12)]
pins = [None for _ in range(12)]
buttons = [None for _ in range(12)]

buttons = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=8,  # TODO: This needs to be configurable.
    value_when_pressed=True)


def init(_):
    """
    Simply clear the controller settings.
    """
    Controller.reset()


def update(df: float):
    event = buttons.events.get()
    if event:
        # event.key_number corresponds to:
        # 0: Up, 1: Down, 2: Left, 3: Right, 4: Select, 5: Start, 6: Button A, 7: Button B
        if event.pressed:
            print(f"Button {event.key_number} was pressed!")

    Controller.update(values)


def deinit():
    """
    Simply clear the controller settings.
    """
    Controller.reset()
