import os
from types import ModuleType

import pgzero.loaders as loaders
from pgzero.game import PGZeroGame

from pmpge.game import Game
from pmpge.game_object import GameObject
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
    Simple test to ensure that DrawImage works.
    """
    setup_pgzero()
    trait = DrawImage("7x3.png")

    assert trait._surface is not None
    assert trait._offset_x == 3
    assert trait._offset_y == 1
    assert trait.image == "7x3.png"
    assert trait._image == "7x3.png"


# noinspection PyUnresolvedReferences
def test_using_with_game_object():
    """
    Validates it can be used as a GameObject trait.
    """
    setup_pgzero()
    game: Game = Game(320, 240)
    go = GameObject(DrawImage("8x8.png"))
    assert go._surface is not None
    assert go._offset_x == 4
    assert go._offset_y == 4
    assert go.image == "8x8.png"
    assert go._image == "8x8.png"
