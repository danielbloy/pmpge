import os
from types import ModuleType

import pgzero.loaders as loaders
from pgzero.game import PGZeroGame

from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage


def setup_pgzero():
    """
    Because a bunch of other tests execute and quit pgzero, there is a strong chance
    the display has been shutdown. We therefore perform a minimal "reboot" along with
    setting the current resource loading directory to the directory of the current test
    file so we can run the tests.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    loaders.set_root(dir_path)

    mod = ModuleType("test")
    PGZeroGame(mod).reinit_screen()


def test_constructor():
    """
    Simple test to ensure that DrawImage works. This pays particular attention to the
    bounding box as we need to adhere to the placement rules.
    """
    setup_pgzero()
    trait = DrawImage("7x3.png")
    assert trait.image.surface is not None
    assert trait.image.width == 7
    assert trait.image.height == 3
    assert trait.bounds.width == 7
    assert trait.bounds.height == 3
    assert trait.bounds.top_left == (-3, -1)
    assert trait.bounds.bottom_right == (3, 1)

    trait = DrawImage("7x7.png")
    assert trait.image.surface is not None
    assert trait.image.width == 7
    assert trait.image.height == 7
    assert trait.bounds.width == 7
    assert trait.bounds.height == 7
    assert trait.bounds.top_left == (-3, -3)
    assert trait.bounds.bottom_right == (3, 3)

    trait = DrawImage("8x8.png")
    assert trait.image.surface is not None
    assert trait.image.width == 8
    assert trait.image.height == 8
    assert trait.bounds.width == 8
    assert trait.bounds.height == 8
    assert trait.bounds.top_left == (-4, -4)
    assert trait.bounds.bottom_right == (3, 3)


# noinspection PyUnresolvedReferences
def test_using_with_game_object():
    """
    Validates it can be used as a GameObject trait.
    """
    setup_pgzero()
    game: Game = Game(320, 240)
    go = GameObject(DrawImage("8x8.png"))
    assert go.image.surface is not None
    assert go.image.width == 8
    assert go.image.height == 8
    assert go.bounds.width == 8
    assert go.bounds.height == 8
    assert go.bounds.top_left == (-4, -4)
    assert go.bounds.bottom_right == (3, 3)

    go = Sprite(10, 20, DrawImage("8x8.png"))
    assert go.x == 10
    assert go.y == 20
    assert go.image.surface is not None
    assert go.image.width == 8
    assert go.image.height == 8
    assert go.bounds.width == 8
    assert go.bounds.height == 8
    assert go.bounds.top_left == (-4, -4)
    assert go.bounds.bottom_right == (3, 3)
    go.update_hierarchy(0)
    assert go.bounds.top_left == (6, 16)
    assert go.bounds.bottom_right == (13, 23)
