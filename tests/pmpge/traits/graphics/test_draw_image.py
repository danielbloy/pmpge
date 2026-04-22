from pygments.lexers import go

from pmpge.game_object import GameObject
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import Position
from tests.pmpge.test_utilities import setup_pgzero


def test_constructor():
    """
    Simple test to ensure that DrawImage works.
    """
    setup_pgzero(__file__)
    trait = DrawImage("7x3.png")
    assert trait._surface is not None
    assert trait._offset_x == 3
    assert trait._offset_y == 1
    assert trait._image == "7x3.png"
    assert trait.image == "7x3.png"

    trait = DrawImage("7x7.png")
    assert trait._surface is not None
    assert trait._offset_x == 3
    assert trait._offset_y == 3
    assert trait._image == "7x7.png"
    assert trait.image == "7x7.png"

    trait = DrawImage("8x8.png")
    assert trait._surface is not None
    assert trait._offset_x == 4
    assert trait._offset_y == 4
    assert trait._image == "8x8.png"
    assert trait.image == "8x8.png"


# noinspection PyUnresolvedReferences
def test_changing_image():
    """
    Validates that the image can be changed.
    """
    setup_pgzero(__file__)
    go = GameObject(DrawImage("8x8.png"))
    assert go._surface is not None
    assert go._offset_x == 4
    assert go._offset_y == 4
    assert go._image == "8x8.png"
    assert go.image == "8x8.png"

    go.update_hierarchy(0)
    assert go._surface is not None
    assert go._offset_x == 4
    assert go._offset_y == 4
    assert go._image == "8x8.png"
    assert go.image == "8x8.png"

    go.image = "7x3.png"
    assert go._surface is not None
    assert go._offset_x == 4
    assert go._offset_y == 4
    assert go._image == "8x8.png"
    assert go.image == "7x3.png"

    go.update_hierarchy(0)
    assert go._surface is not None
    assert go._offset_x == 3
    assert go._offset_y == 1
    assert go._image == "7x3.png"
    assert go.image == "7x3.png"


def test_using_with_game_object():
    """
    Validates it can be used as a GameObject trait.
    """
    setup_pgzero(__file__)
    go = GameObject(DrawImage("8x8.png"))
    assert go._surface is not None
    assert go._offset_x == 4
    assert go._offset_y == 4
    assert go._image == "8x8.png"
    assert go.image == "8x8.png"
    go.update_hierarchy(0)

    go = GameObject(Position(10, 20), DrawImage("7x3.png"))
    assert go._surface is not None
    assert go._offset_x == 3
    assert go._offset_y == 1
    assert go._image == "7x3.png"
    assert go.image == "7x3.png"
    go.update_hierarchy(0)

# TODO: Add test to draw to draw the object
