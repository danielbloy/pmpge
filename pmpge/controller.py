"""
The controller configuration is based on 12 button SNES controller as follows:

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

__controller = environment.import_driver('controller')


# Support the following events:
#   button_pressed
#   button_released
# FUTURE: Repeat

# TODO: Need a way to get information about the buttons supported by the device.

class Controller:
    """
    The controller only has static values.
    """
    start: bool = False
    select: bool = False

    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False

    l: bool = False
    r: bool = False
    u: bool = False
    d: bool = False

    left_shoulder: bool = False
    right_shoulder: bool = False

    ls: bool = False
    rs: bool = False

    a: bool = False
    b: bool = False
    x: bool = False
    y: bool = False
