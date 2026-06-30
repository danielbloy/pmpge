"""
Creates a range of sprites and moves then around the screen. This
is useful for validating movement, smoothness and performance. This
uses the baseline test data.
"""
import validate.utils as utils
from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.traits.controller import MoveWithController
from pmpge.traits.position import BoundPosition
from validate.test_data import SpriteData, create_sprites

SCREEN_WIDTH = 80  # Results in a border of 40 pixels left and right
SCREEN_HEIGHT = 60  # Results in a border of 14 pixels top and bottom


def setup(game: Game):
    game.background_colour = (120, 120, 0)  # Green

    items: list[SpriteData] = [
        SpriteData(10, 15, "alien_e.png"),
        SpriteData(40, 15, "alien_d.png"),
        SpriteData(70, 15, "alien_c.png"),
        # SpriteData(10, 15, "alien_b.png"),
        # SpriteData(40, 15, "alien.png"),
        SpriteData(20, 45, "earth.png"),
        SpriteData(20, 45, "john.png"),
        SpriteData(50, 45, "john.png"),
    ]
    create_sprites(game, items)

    hero_data = SpriteData(game.width // 2, game.height // 2, "john.png", vx=0, vy=0)
    create_sprites(game, [hero_data])
    controller = Controller()
    hero_data.sprite.apply_trait(MoveWithController(controller, 60, 60))
    hero_data.sprite.apply_trait(BoundPosition(8, 8, game.width - 8, game.height - 8))

    # TODO: oscilate an alien over the aliens.


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
