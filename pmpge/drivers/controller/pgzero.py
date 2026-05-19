"""
Defines the controller by mapping to the Pygame Zero keyboard instance.
"""

from pgzero.builtins import keyboard

from pmpge.controller import Controller


# FUTURE: Allow the button configuration to be specified in config.


def update(dt: float):
    # TODO: Do something about having to set left and l etc.
    
    Controller.start = keyboard.RETURN or keyboard.space
    Controller.select = keyboard.escape

    Controller.l = keyboard.a or keyboard.left
    Controller.r = keyboard.d or keyboard.right
    Controller.u = keyboard.w or keyboard.up
    Controller.d = keyboard.s or keyboard.down
    Controller.left = Controller.l
    Controller.right = Controller.r
    Controller.up = Controller.u
    Controller.down = Controller.d

    Controller.a = keyboard.l
    Controller.b = keyboard.k
    Controller.x = keyboard.i
    Controller.y = keyboard.j

    Controller.ls = keyboard.q
    Controller.rs = keyboard.p
    Controller.left_shoulder = Controller.ls
    Controller.right_shoulder = Controller.rs
