"""
This is a test controller using Pygame zero and the keyboard to provide
a simple AB controller with 4 buttons.
"""

from pgzero.builtins import keyboard


class ControllerButtons:

    @property
    def start(self) -> bool:
        return keyboard.enter or keyboard.space

    @property
    def select(self) -> bool:
        return keyboard.escape

    @property
    def l(self) -> bool:
        return keyboard.k

    @property
    def r(self) -> bool:
        return keyboard.l

    @property
    def u(self) -> bool:
        return False

    @property
    def d(self) -> bool:
        return False
