from dataclasses import dataclass

import pytest

from pmpge.game_object import GameObject
from pmpge.traits.controller import MoveWithController
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position


@dataclass
class ControllerWith2Buttons:
    left: bool
    right: bool

    @property
    def button_count(self) -> int:
        return 2


@dataclass
class ControllerWith4Buttons:  # This will have A and B buttons as well as left and right
    left: bool
    right: bool
    up: bool  # wont be used
    down: bool  # wont be used

    @property
    def button_count(self) -> int:
        return 4


@dataclass
class ControllerWith6Buttons:
    left: bool
    right: bool
    up: bool
    down: bool

    @property
    def button_count(self) -> int:
        return 6


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    controller = ControllerWith2Buttons(False, False)
    trait = MoveWithController(0, 0, controller)
    assert trait.mx == 0
    assert trait.my == 0
    assert trait.controller == controller

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0

    controller = ControllerWith4Buttons(False, False, False, False)
    trait = MoveWithController(10, 20, controller)
    assert trait.mx == 10
    assert trait.my == 20
    assert trait.controller == controller

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0

    controller = ControllerWith4Buttons(False, False, False, False)
    trait = MoveWithController(-1, -2, controller)
    assert trait.mx == -1
    assert trait.my == -2
    assert trait.controller == controller

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0


def test_without_position():
    """
    Validates a Position trait with required.
    """
    controller = ControllerWith4Buttons(False, False, False, False)
    go = GameObject(MoveWithController(10, 20, controller))
    with pytest.raises(AttributeError):
        go.update_hierarchy(0)


# noinspection PyUnresolvedReferences
def test_with_2_buttons():
    """
    Validates that horizontal movement works with only a 2 button controller
    """
    controller = ControllerWith2Buttons(False, False)
    go = GameObject(Position(0, 0), MoveWithController(10, 20, controller))
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Should change nothing
    controller.left = True
    controller.right = True
    go.update_hierarchy(0)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Right
    controller.left = False
    controller.right = True
    go.update_hierarchy(1)
    assert go.x == 10
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left
    controller.left = True
    controller.right = False
    go.update_hierarchy(1.5)
    assert go.x == -5
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Right again
    controller.left = False
    controller.right = True
    go.update_hierarchy(1.5)
    assert go.x == 10
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left again
    controller.left = True
    controller.right = False
    go.update_hierarchy(1)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left and right (left wins)
    controller.left = True
    controller.right = True
    go.update_hierarchy(1)
    assert go.x == -10
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20


# noinspection PyUnresolvedReferences
def test_with_4_buttons():
    """
    Validates that only horizontal movement works with a 4 button controller.
    """
    controller = ControllerWith4Buttons(False, False, False, False)
    go = GameObject(Position(0, 0), MoveWithController(10, 20, controller))
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Should change nothing
    controller.left = True
    controller.right = True
    controller.up = True
    controller.down = True
    go.update_hierarchy(0)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Right works
    controller.left = False
    controller.right = True
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 10
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left works
    controller.left = True
    controller.right = False
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Down does not work
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = True
    go.update_hierarchy(1)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Up does not work
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20


# noinspection PyUnresolvedReferences
def test_with_6_buttons():
    """
    Validates horizontal and vertical movement works with a 6 button controller.
    """
    controller = ControllerWith6Buttons(False, False, False, False)
    go = GameObject(Position(0, 0), MoveWithController(10, 20, controller))
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Should change nothing
    controller.left = True
    controller.right = True
    controller.up = True
    controller.down = True
    go.update_hierarchy(0)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Right
    controller.left = False
    controller.right = True
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 10
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left
    controller.left = True
    controller.right = False
    controller.up = False
    controller.down = False
    go.update_hierarchy(1.5)
    assert go.x == -5
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left and right (left wins)
    controller.left = True
    controller.right = True
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == -15
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Down
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = True
    go.update_hierarchy(1)
    assert go.x == -15
    assert go.y == 20
    assert go.mx == 10
    assert go.my == 20

    # Up
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = False
    go.update_hierarchy(1.5)
    assert go.x == -15
    assert go.y == -10
    assert go.mx == 10
    assert go.my == 20

    # Down again
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = True
    go.update_hierarchy(1)
    assert go.x == -15
    assert go.y == 10
    assert go.mx == 10
    assert go.my == 20

    # Up again
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = False
    go.update_hierarchy(1.5)
    assert go.x == -15
    assert go.y == -20
    assert go.mx == 10
    assert go.my == 20

    # Down and up (up wins)
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = True
    go.update_hierarchy(1)
    assert go.x == -15
    assert go.y == -40
    assert go.mx == 10
    assert go.my == 20

    # Reset and all buttons are set
    go.x = 0
    go.y = 0
    controller.left = True
    controller.right = True
    controller.up = True
    controller.down = True
    go.update_hierarchy(1)
    assert go.x == -10
    assert go.y == -20
    assert go.mx == 10
    assert go.my == 20


# noinspection PyUnresolvedReferences
def test_velocity_and_move_with_controller():
    """
    This runs a small number of tests when Velocity is combined with MoveWithController.
    Order matters so in these tests, Velocity is processed first.
    """
    controller = ControllerWith6Buttons(False, False, False, False)
    go = GameObject(
        Position(0, 0),
        Velocity(30, 40),
        MoveWithController(10, 20, controller)
    )
    assert go.x == 0
    assert go.y == 0
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20

    # Should change nothing
    controller.left = True
    controller.right = True
    controller.up = True
    controller.down = True
    go.update_hierarchy(0)
    assert go.x == 0
    assert go.y == 0
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20

    # Velocity should move the GameObject
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 30
    assert go.y == 40
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20

    # Velocity and right should move the GameObject
    controller.left = False
    controller.right = True
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 70
    assert go.y == 80
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20

    # Velocity and left should move the GameObject
    controller.left = True
    controller.right = False
    controller.up = False
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 90
    assert go.y == 120
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20

    # Velocity and down should move the GameObject
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = True
    go.update_hierarchy(1)
    assert go.x == 120
    assert go.y == 180
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20

    # Velocity and up should move the GameObject
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = False
    go.update_hierarchy(1)
    assert go.x == 150
    assert go.y == 200
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20
