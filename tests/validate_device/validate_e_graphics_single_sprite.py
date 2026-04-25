"""
Creates a single sprite and moves it on the screen. This should work
on all devices as there are no implementation specific details here.
"""
import tests.validate_device.utils as utils

from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.physics import Velocity
from pmpge.traits.sprites import SpriteImage


def setup(game: Game):
    sprite = Sprite(
        20, 10,
        Velocity(20, 20),
        SpriteImage("player.png"))
    game.add_child(sprite)


if utils.should_execute(__name__):
    utils.execute(setup)
