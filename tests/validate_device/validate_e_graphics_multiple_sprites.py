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
    SpriteData(0, 0, 5, 5, "player.png"),
    SpriteData(10, 10, 10, 10, "alien.png"),
    SpriteData(100, 10, -5, 20, "alien_b.png"),
    SpriteData(10, 10, 5, -25, "alien_c.png"),
    SpriteData(20, 20, -15, 15, "alien_d.png"),
    SpriteData(30, 30, 25, -5, "alien_e.png"),
    SpriteData(40, 40, -5, 25, "alien_f.png"),
    SpriteData(50, 50, 15, -15, "alien_g.png"),
    SpriteData(60, 60, -25, 5, "alien_h.png"),
    SpriteData(80, 60, 5, 5, "bomb.png"),
    SpriteData(80, 60, -5, -5, "laser.png"),
    SpriteData(80, 60, -5, 5, "marker.png"),
    SpriteData(80, 60, 5, -5, "7x3.png"),
    SpriteData(80, 60, 15, 15, "7x7.png"),
    SpriteData(80, 60, -15, -15, "8x8.png"),
    SpriteData(80, 60, -15, 15, "7x3.png"),
    SpriteData(80, 60, 15, -15, "7x7.png"),
    SpriteData(60, 118, 5, -20, "8x8.png"),
    SpriteData(150, 118, -10, -10, "alien_g.png"),
    SpriteData(160, 128, -5, -5, "alien_h.png"),
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
