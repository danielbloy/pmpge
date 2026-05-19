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


class Controller:
    """
    The controller only has static values. This allows multiple instances of
    controller to share the values.

    # TODO: The only danger here is that these should be read-only so maybe replace
    #       with _l etc. and use read-only properties for the named entries.
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


__controller = environment.import_driver('controller')


# TODO: Call the driver to get the button statuses which returns a tuple of
#       values (which it can update in the driver update() function).

# TODO: The Controller needs to be regularly polled so that it can generate events.
#       Should we do this as a GameObject?
#       We do however want to avoid a use having to run boiler plate.

# Actually, we could create the events as a GameObject and hook into the game. This
# then allows for events to make use of activated etc. This will make it easy to have
# different event handlers at different parts of the game.

# TODO: Actually, this could even be done as a Trait and simply attached to a GameObject.

class ControllerEvents:
    pass

# controller.on_start_pressed = <event>
# controller.on_start_released = <event>
#

# TODO: Controller can provide a class to return which buttons changed since the
#       last update with rise and fall a bit like Adafruits debouncer.


# TODO: Combine ControllerEvents with GameObject much like with Sprites.

#
# TODO: The Controller needs to contain the buttons.


# Support the following events:
#   button_pressed
#   button_released
# FUTURE: Repeat

# TODO: Need a way to get information about the buttons supported by the device.
