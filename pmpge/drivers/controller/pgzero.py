"""
Defines the controller by mapping to the Pygame Zero keyboard instance.
"""

from pgzero.builtins import keyboard


# FUTURE: Allow the button configuration to be specified in config.

class ControllerButtons:
    """
    This is a simple controller that uses the Pygame Zero keyboard and provides the
    full keyboard mapping for the SNES controller.
    """

    @property
    def start(self) -> bool:
        return keyboard.enter or keyboard.space

    @property
    def select(self) -> bool:
        return keyboard.escape

    @property
    def l(self) -> bool:
        return keyboard.a or keyboard.left

    @property
    def r(self) -> bool:
        return keyboard.d or keyboard.right

    @property
    def u(self) -> bool:
        return keyboard.w or keyboard.up

    @property
    def d(self) -> bool:
        return keyboard.s or keyboard.down

    @property
    def a(self) -> bool:
        return keyboard.l

    @property
    def b(self) -> bool:
        return keyboard.k

    @property
    def x(self) -> bool:
        return keyboard.i

    @property
    def y(self) -> bool:
        return keyboard.j

    @property
    def ls(self) -> bool:
        return keyboard.q

    @property
    def rs(self) -> bool:
        return keyboard.p
