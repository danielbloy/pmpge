"""
Creates many sprites and moves them around on the screen. This should work
on all devices as there are no implementation specific details here.
"""
import tests.validate_device.utils as utils

from pmpge.game import Game

sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(0, 0, 5, 5, "player.png"),
    utils.SpriteData(10, 10, 10, 10, "alien.png"),
    utils.SpriteData(100, 10, -5, 20, "alien_b.png"),
    utils.SpriteData(10, 10, 5, -25, "alien_c.png"),
    utils.SpriteData(20, 20, -15, 15, "alien_d.png"),
    utils.SpriteData(30, 30, 25, -5, "alien_e.png"),
    utils.SpriteData(40, 40, -5, 25, "alien_f.png"),
    utils.SpriteData(50, 50, 15, -15, "alien_g.png"),
    utils.SpriteData(60, 60, -25, 5, "alien_h.png"),
    utils.SpriteData(80, 60, 5, 5, "bomb.png"),
    utils.SpriteData(80, 60, -5, -5, "laser.png"),
    utils.SpriteData(80, 60, -5, 5, "marker.png"),
    utils.SpriteData(80, 60, 5, -5, "7x3.png"),
    utils.SpriteData(80, 60, 15, 15, "7x7.png"),
    utils.SpriteData(80, 60, -15, -15, "8x8.png"),
    utils.SpriteData(80, 60, -15, 15, "7x3.png"),
    utils.SpriteData(80, 60, 15, -15, "7x7.png"),
    utils.SpriteData(60, 118, 5, -20, "8x8.png"),
    utils.SpriteData(150, 118, -10, -10, "alien_g.png"),
    utils.SpriteData(160, 128, -5, -5, "alien_h.png"),
]


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.create_sprites(game, sprite_data)


if utils.should_execute(__name__):
    utils.execute(setup)
