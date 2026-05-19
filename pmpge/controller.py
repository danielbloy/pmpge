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
    The controller has static values that the underlying driver sets.
    This allows multiple instances of controller to share the values.
    There are instance properties that are read only that expose the
    underlying values.
    """
    _start: bool = False
    _select: bool = False

    _l: bool = False
    _r: bool = False
    _u: bool = False
    _d: bool = False

    _ls: bool = False
    _rs: bool = False

    _a: bool = False
    _b: bool = False
    _x: bool = False
    _y: bool = False

    @property
    def start(self) -> bool:
        return Controller._start

    @property
    def select(self) -> bool:
        return Controller._select

    @property
    def left(self) -> bool:
        return Controller._l

    @property
    def l(self) -> bool:
        return Controller._l

    @property
    def right(self) -> bool:
        return Controller._r

    @property
    def r(self) -> bool:
        return Controller._r

    @property
    def up(self) -> bool:
        return Controller._u

    @property
    def u(self) -> bool:
        return Controller._u

    @property
    def down(self) -> bool:
        return Controller._d

    @property
    def d(self) -> bool:
        return Controller._d

    @property
    def a(self) -> bool:
        return Controller._a

    @property
    def b(self) -> bool:
        return Controller._b

    @property
    def x(self) -> bool:
        return Controller._x

    @property
    def y(self) -> bool:
        return Controller._y

    @property
    def left_shoulder(self) -> bool:
        return Controller._ls

    @property
    def ls(self) -> bool:
        return Controller._ls

    @property
    def right_shoulder(self) -> bool:
        return Controller._rs

    @property
    def rs(self) -> bool:
        return Controller._rs


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
