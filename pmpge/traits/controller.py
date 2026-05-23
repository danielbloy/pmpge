#
# All of the controller traits take a controller instance as their first
# parameter. When these traits are applied to a GameObject, only one of
# the controller instance variables is copied across. This is by design
# but does mean that only a single Controller instance can be used (again
# this isn't much of a practical limitation).
#

from pmpge.controller import Controller
from pmpge.environment import is_running_on_desktop
from pmpge.game_object import GameObject

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable


class MoveWithController:
    """
    MoveWithController uses a Controller object to move the GameObject either
    horizontally, vertically or both by a specified velocity in pixels per second.

    The Controller must have a left and right button but can optionally have up
    and down buttons. This allows it to be used with 2 button controllers and up.

    The MoveWithController trait requires a Position trait to be present on the
    GameObject.
    """

    x: float
    y: float
    mx: int
    my: int
    controller: Controller

    def __init__(self, controller: Controller, mx, my: int):
        self.mx = mx
        self.my = my
        self.controller = controller

    def update(self, dt: float):
        new_x = self.x
        new_y = self.y
        controller = self.controller

        if controller.left:
            new_x -= (self.mx * dt)
        elif controller.right:
            new_x += (self.mx * dt)

        if controller.up:
            new_y -= (self.my * dt)
        elif controller.down:
            new_y += (self.my * dt)

        self.x = new_x
        self.y = new_y


class OnPressed:
    """
    Responds to multiple OnPressed events for the specified buttons. Each event pass in
    should be a tuple contains two items:
      * The button as one of the constants on Controller
      * A callable to invoke when the button was pressed
    """
    controller: Controller
    on_pressed: tuple[tuple[int, Callable[[GameObject], None]]]

    def __init__(self, controller: Controller, *events: tuple[int, Callable[[GameObject], None]]):
        self.controller = controller
        # noinspection PyTypeChecker
        self.on_pressed = events

    def update(self, dt: float):
        for on_pressed in self.on_pressed:
            if self.controller.has_pressed(on_pressed[0]):
                # noinspection PyTypeChecker
                on_pressed[1](self)


class OnReleased:
    """
    Responds to multiple OnReleased events for the specified buttons. Each event pass in
    should be a tuple contains two items:
      * The button as one of the constants on Controller
      * A callable to invoke when the button was released
    """
    controller: Controller
    on_released: tuple[tuple[int, Callable[[GameObject], None]]]

    def __init__(self, controller: Controller, *events: tuple[int, Callable[[GameObject], None]]):
        self.controller = controller
        # noinspection PyTypeChecker
        self.on_released = events

    def update(self, dt: float):
        for on_released in self.on_released:
            if self.controller.has_released(on_released[0]):
                # noinspection PyTypeChecker
                on_released[1](self)
