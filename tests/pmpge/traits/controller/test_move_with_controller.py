from dataclasses import dataclass

import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.traits.controller import MoveWithController
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position


@dataclass
class ControllerLRUD:
    left: bool
    right: bool
    up: bool
    down: bool


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    controller = ControllerLRUD(False, False, False, False)
    trait = MoveWithController(controller, 0, 0)
    assert trait.mx == 0
    assert trait.my == 0
    assert trait.controller == controller

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0

    controller = ControllerLRUD(False, False, False, False)
    trait = MoveWithController(controller, 10, 20)
    assert trait.mx == 10
    assert trait.my == 20
    assert trait.controller == controller

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0

    controller = ControllerLRUD(False, False, False, False)
    trait = MoveWithController(controller, -1, -2)
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
    controller = ControllerLRUD(False, False, False, False)
    go = GameObject(MoveWithController(controller, 10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


# noinspection PyUnresolvedReferences
def test_with_lrud_buttons():
    """
    Validates horizontal and vertical movement works with a controller that supports
    left, right , up and down buttons.
    """
    controller = ControllerLRUD(False, False, False, False)
    go = GameObject(Position(0, 0), MoveWithController(controller, 10, 20))
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Should change nothing
    controller.left = True
    controller.right = True
    controller.up = True
    controller.down = True
    update_hierarchy(go, 0)
    assert go.x == 0
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Right
    controller.left = False
    controller.right = True
    controller.up = False
    controller.down = False
    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left
    controller.left = True
    controller.right = False
    controller.up = False
    controller.down = False
    update_hierarchy(go, 1.5)
    assert go.x == -5
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Left and right (left wins)
    controller.left = True
    controller.right = True
    controller.up = False
    controller.down = False
    update_hierarchy(go, 1)
    assert go.x == -15
    assert go.y == 0
    assert go.mx == 10
    assert go.my == 20

    # Down
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = True
    update_hierarchy(go, 1)
    assert go.x == -15
    assert go.y == 20
    assert go.mx == 10
    assert go.my == 20

    # Up
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = False
    update_hierarchy(go, 1.5)
    assert go.x == -15
    assert go.y == -10
    assert go.mx == 10
    assert go.my == 20

    # Down again
    controller.left = False
    controller.right = False
    controller.up = False
    controller.down = True
    update_hierarchy(go, 1)
    assert go.x == -15
    assert go.y == 10
    assert go.mx == 10
    assert go.my == 20

    # Up again
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = False
    update_hierarchy(go, 1.5)
    assert go.x == -15
    assert go.y == -20
    assert go.mx == 10
    assert go.my == 20

    # Down and up (up wins)
    controller.left = False
    controller.right = False
    controller.up = True
    controller.down = True
    update_hierarchy(go, 1)
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
    update_hierarchy(go, 1)
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
    controller = ControllerLRUD(False, False, False, False)
    go = GameObject(
        Position(0, 0),
        Velocity(30, 40),
        MoveWithController(controller, 10, 20)
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
    update_hierarchy(go, 0)
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
    update_hierarchy(go, 1)
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
    update_hierarchy(go, 1)
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
    update_hierarchy(go, 1)
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
    update_hierarchy(go, 1)
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
    update_hierarchy(go, 1)
    assert go.x == 150
    assert go.y == 200
    assert go.vx == 30
    assert go.vy == 40
    assert go.mx == 10
    assert go.my == 20
