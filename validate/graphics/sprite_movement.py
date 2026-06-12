"""
Creates sprites and moves them around on the screen, alternating visibility.
"""
import validate.utils as utils
from pmpge.game import Game
from pmpge.utilities import add_rate_limited_func
from validate import test_data

sprite_data: list[test_data.SpriteData] = [
    test_data.SpriteData(80, 60, "alien.png", 15, 0),
    test_data.SpriteData(80, 60, "alien_b.png", -15, 0),
    test_data.SpriteData(80, 60, "alien_c.png", 0, 15),
    test_data.SpriteData(80, 60, "alien_d.png", 0, -15),
    test_data.SpriteData(80, 60, "alien_e.png", 15, 15),
    test_data.SpriteData(80, 60, "alien_f.png", -15, -15),
    test_data.SpriteData(80, 60, "alien_g.png", 15, -15),
    test_data.SpriteData(80, 60, "alien_h.png", -15, 15),
]

index = 0
count = len(sprite_data)


def switch_visibility(_: float):
    global index
    sprite_data[index].sprite.visible = True
    index = (index + 1) % count
    sprite_data[index].sprite.visible = False


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    test_data.create_sprites(game, sprite_data)
    add_rate_limited_func(game, switch_visibility)


if utils.should_execute(__name__):
    utils.execute(setup)
