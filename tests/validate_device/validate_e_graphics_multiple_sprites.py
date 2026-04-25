"""
Creates many sprites and moves them around on the screen. This should work
on all devices as there are no implementation specific details here.
"""
import tests.validate_device.utils as utils

from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.physics import Velocity
from pmpge.traits.sprites import SpriteImage


class SpriteData:
    x: int
    y: int
    vx: int
    vy: int
    image: str

    def __init__(self, x: int, y: int, vx: int, vy: int, image: str):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image = image


sprite_data: list[SpriteData] = [
    SpriteData(0, 0, 5, 5, "player.png")
]


def setup(game: Game):
    for data in sprite_data:
        sprite = Sprite(
            data.x, data.y,
            Velocity(data.vx, data.vy),
            SpriteImage(data.image))
        game.add_child(sprite)


if utils.should_execute(__name__):
    utils.execute(setup)
