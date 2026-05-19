"""
Defines the controller by mapping to the Pygame Zero keyboard instance.
"""

from pgzero.builtins import keyboard

from pmpge.controller import Controller


# FUTURE: Allow the button configuration to be specified in config.


def update(dt: float):
    Controller._start = keyboard.RETURN or keyboard.space
    Controller._select = keyboard.escape

    Controller._l = keyboard.a or keyboard.left
    Controller._r = keyboard.d or keyboard.right
    Controller._u = keyboard.w or keyboard.up
    Controller._d = keyboard.s or keyboard.down

    Controller._a = keyboard.l
    Controller._b = keyboard.k
    Controller._x = keyboard.i
    Controller._y = keyboard.j

    Controller._ls = keyboard.q
    Controller._rs = keyboard.p
