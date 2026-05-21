"""
Defines the controller by mapping to the Pygame Zero keyboard instance.
"""

from pgzero.builtins import keyboard

from pmpge.controller import Controller

# FUTURE: Allow the button configuration to be specified in config.

values: list[bool] = [False for _ in range(12)]


def update(dt: float):
    values[0] = keyboard.RETURN or keyboard.space
    values[1] = keyboard.escape

    values[2] = keyboard.a or keyboard.left
    values[3] = keyboard.d or keyboard.right
    values[4] = keyboard.w or keyboard.up
    values[5] = keyboard.s or keyboard.down

    values[6] = keyboard.l
    values[7] = keyboard.k
    values[8] = keyboard.i
    values[9] = keyboard.j

    values[10] = keyboard.q
    values[11] = keyboard.p

    Controller.update(values)
