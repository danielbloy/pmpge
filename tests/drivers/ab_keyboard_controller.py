"""
This is a test controller using Pygame zero and the keyboard to provide
a simple AB controller with 4 buttons.
"""

from pgzero.builtins import keyboard

from pmpge.controller import ABController


class Controller(ABController):

    @property
    def start(self) -> bool:
        return keyboard.enter or keyboard.space

    @property
    def select(self) -> bool:
        return keyboard.escape

    @property
    def a(self) -> bool:
        return keyboard.l

    @property
    def b(self) -> bool:
        return keyboard.k
