"""
This is a test hal using Pygame zero and a reduce controller set.
"""

from pgzero.builtins import keyboard

from pgzge.controller import ABController


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
