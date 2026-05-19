"""
The controller configuration is based on 12 button SNES controller as follows:

 L Shoulder   R Shoulder

      U           X
    L   R       Y   A
      D           B

    Start       Select

Because the range of devices varies, so does the number of buttons available so all
devices may not support the 12 set of 12 buttons. Common other configurations include:

10 button SNES controller without shoulder buttons:

      U           X
    L   R       Y   A
      D           B

    Start       Select

8 button NES:

      U
    L   R           A
      D           B

    Start       Select

There are lots of other configurations possible too depending on the device.
"""

import pmpge.environment as environment


# FUTURE: Add support for a second players controller
# FUTURE: Add support for a on_repeat event


class Controller:
    """
    The controller has static values that the underlying driver sets.
    This allows multiple instances of controller to share the values.
    There are instance properties that are read only that expose the
    underlying values.
    """
    current: list[bool] = [False for _ in range(12)]  # Current button values
    changed: list[bool] = [False for _ in range(12)]  # Have buttons changed?

    __previous: list[bool] = [False for _ in range(12)]

    BUTTON_START: int = 0
    BUTTON_SELECT: int = 1
    BUTTON_LEFT: int = 2
    BUTTON_RIGHT: int = 3
    BUTTON_UP: int = 4
    BUTTON_DOWN: int = 5
    BUTTON_A: int = 6
    BUTTON_B: int = 7
    BUTTON_X: int = 8
    BUTTON_Y: int = 9
    BUTTON_LS: int = 10
    BUTTON_RS: int = 11

    @staticmethod
    def update():
        current = Controller.current
        previous = Controller.__previous
        changed = Controller.changed

        # Determine if changed
        for i in range(12):
            changed[i] = current[i] != previous[i]

        # Copy new values
        for i in range(12):
            previous[i] = current[i]

    @property
    def start(self) -> bool:
        return Controller.current[0]

    @property
    def select(self) -> bool:
        return Controller.current[1]

    @property
    def left(self) -> bool:
        return Controller.current[2]

    @property
    def l(self) -> bool:
        return Controller.current[2]

    @property
    def right(self) -> bool:
        return Controller.current[3]

    @property
    def r(self) -> bool:
        return Controller.current[3]

    @property
    def up(self) -> bool:
        return Controller.current[4]

    @property
    def u(self) -> bool:
        return Controller.current[4]

    @property
    def down(self) -> bool:
        return Controller.current[5]

    @property
    def d(self) -> bool:
        return Controller.current[5]

    @property
    def a(self) -> bool:
        return Controller.current[6]

    @property
    def b(self) -> bool:
        return Controller.current[7]

    @property
    def x(self) -> bool:
        return Controller.current[8]

    @property
    def y(self) -> bool:
        return Controller.current[9]

    @property
    def left_shoulder(self) -> bool:
        return Controller.current[10]

    @property
    def ls(self) -> bool:
        return Controller.current[10]

    @property
    def right_shoulder(self) -> bool:
        return Controller.current[11]

    @property
    def rs(self) -> bool:
        return Controller.current[11]


__controller = environment.import_driver('controller')
