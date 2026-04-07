"""
Defines the controller by mapping to the Pygame Zero keyboard instance.
"""

from pgzero.builtins import keyboard

from pmpge.controller import SNESController


class Controller(SNESController):

    # TODO: Document this class
    # TODO: Test this class
    # TODO: Optionally specify the controller buttons in config as an array.
    #       The number of buttons determines the size of the controller.
    #       This could be common code across all systems as it just needs
    #       a property for true or false for pressed/no pressed. Then another
    #       for a button event.

    @property
    def start(self) -> bool:
        return keyboard.enter or keyboard.space

    @property
    def select(self) -> bool:
        return keyboard.escape

    @property
    def left(self) -> bool:
        return keyboard.a or keyboard.left

    @property
    def right(self) -> bool:
        return keyboard.d or keyboard.right

    @property
    def up(self) -> bool:
        return keyboard.w or keyboard.up

    @property
    def down(self) -> bool:
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
    def left_shoulder(self) -> bool:
        return keyboard.q

    @property
    def right_shoulder(self) -> bool:
        return keyboard.p
