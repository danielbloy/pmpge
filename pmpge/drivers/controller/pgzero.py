"""
Defines the controller by mapping to the Pygame Zero keyboard instance.
"""

from pgzero.builtins import keyboard

from pmpge.controller import Controller


# FUTURE: Allow the button configuration to be specified in config.


def update(dt: float):
    current = Controller.current
    current[0] = keyboard.RETURN or keyboard.space
    current[1] = keyboard.escape

    current[2] = keyboard.a or keyboard.left
    current[3] = keyboard.d or keyboard.right
    current[4] = keyboard.w or keyboard.up
    current[5] = keyboard.s or keyboard.down

    current[6] = keyboard.l
    current[7] = keyboard.k
    current[8] = keyboard.i
    current[9] = keyboard.j

    current[10] = keyboard.q
    current[11] = keyboard.p

    Controller.update()
