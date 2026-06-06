"""
Creates many sprites and moves them around on the screen.
This shows how well the device copes with 20 on-screen sprites.
"""
import tests.validate_device.utils as utils

from pmpge.game import Game

sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(0, 0, "player.png", 5, 5),
    utils.SpriteData(10, 10, "alien.png", 10, 10),
    utils.SpriteData(100, 10, "alien_b.png", -5, 20),
    utils.SpriteData(10, 10, "alien_c.png", 5, -25),
    utils.SpriteData(20, 20, "alien_d.png", -15, 15),
    utils.SpriteData(30, 30, "alien_e.png", 25, -5),
    utils.SpriteData(40, 40, "alien_f.png", -5, 25),
    utils.SpriteData(50, 50, "alien_g.png", 15, -15),
    utils.SpriteData(60, 60, "alien_h.png", -25, 5),
    utils.SpriteData(80, 60, "bomb.png", 5, 5),
    utils.SpriteData(80, 60, "laser.png", -5, -5),
    utils.SpriteData(80, 60, "marker.png", -5, 5),
    utils.SpriteData(80, 60, "7x3.png", 5, -5),
    utils.SpriteData(80, 60, "7x7.png", 15, 15),
    utils.SpriteData(80, 60, "8x8.png", -15, -15),
    utils.SpriteData(80, 60, "7x3.png", -15, 15),
    utils.SpriteData(80, 60, "7x7.png", 15, -15),
    utils.SpriteData(60, 118, "8x8.png", 5, -20),
    utils.SpriteData(150, 118, "alien_g.png", -10, -10),
    utils.SpriteData(160, 128, "alien_h.png", -5, -5),
]


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.create_sprites(game, sprite_data)


if utils.should_execute(__name__):
    utils.execute(setup)
