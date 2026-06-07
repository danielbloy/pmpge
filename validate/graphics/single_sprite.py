"""
Creates a single sprite and moves it on the screen.
This is useful for judging how smoothly the sprite moves.
"""
import validate_device.utils as utils
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import Velocity


def setup(game: Game):
    sprite = Sprite(
        20, 10,
        Velocity(20, 20),
        DrawImage("player.png"))
    game.add_child(sprite)


if utils.should_execute(__name__):
    utils.execute(setup)
