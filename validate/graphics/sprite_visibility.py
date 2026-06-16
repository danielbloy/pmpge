"""
Creates sprites on the screen, alternating visibility of each item in a
column. This test also uses the same resource for each sprite which can
be used to validate optimisations on image resource sharing.
"""
import validate.utils as utils
from pmpge.game import Game
from pmpge.utilities import add_rate_limited_func
from validate import test_data

sprite_data: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 20, "alien.png"),
    test_data.SpriteData(60, 20, "alien.png"),
    test_data.SpriteData(100, 20, "alien.png"),
    test_data.SpriteData(140, 20, "alien.png"),
    test_data.SpriteData(20, 60, "alien.png"),
    test_data.SpriteData(60, 60, "alien.png"),
    test_data.SpriteData(100, 60, "alien.png"),
    test_data.SpriteData(140, 60, "alien.png"),
    test_data.SpriteData(20, 100, "alien.png"),
    test_data.SpriteData(60, 100, "alien.png"),
    test_data.SpriteData(100, 100, "alien.png"),
    test_data.SpriteData(140, 100, "alien.png"),
]

row_count = 4
index = 0


def switch_visibility(_: float):
    global index

    on = index
    index = (index + 1) % row_count
    off = index

    for modifier in (0, 4, 8):
        sprite_data[on + modifier].sprite.visible = True
        sprite_data[off + modifier].sprite.visible = False


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    test_data.create_sprites(game, sprite_data)
    add_rate_limited_func(game, switch_visibility, rate=4)


if utils.should_execute(__name__):
    utils.execute(setup)
