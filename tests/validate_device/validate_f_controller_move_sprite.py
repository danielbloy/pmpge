"""
Creates sprite in the center of the screen and allows the controller
to move it around. The other buttons toggle the visibility of sprites.
"""

import tests.validate_device.utils as utils
from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.traits.controller import MoveWithController

# The first 12 sprites represent the buttons which have their visibility
# switched as the buttons are preseed. The 13th sprite is the one moved
# around by the controller.
sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(10, 110, 0, 0, "start.png"),
    utils.SpriteData(20, 110, 0, 0, "select.png"),
    utils.SpriteData(30, 110, 0, 0, "left.png"),
    utils.SpriteData(40, 110, 0, 0, "right.png"),
    utils.SpriteData(50, 110, 0, 0, "up.png"),
    utils.SpriteData(60, 110, 0, 0, "down.png"),
    utils.SpriteData(70, 110, 0, 0, "a.png"),
    utils.SpriteData(80, 110, 0, 0, "b.png"),
    utils.SpriteData(90, 110, 0, 0, "x.png"),
    utils.SpriteData(100, 110, 0, 0, "y.png"),
    utils.SpriteData(110, 110, 0, 0, "ls.png"),
    utils.SpriteData(120, 110, 0, 0, "rs.png"),
    utils.SpriteData(80, 60, 0, 0, "hero.png"),
]

index = 0
count = len(sprite_data)


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.create_sprites(game, sprite_data)

    # TODO: Create sprites for buttons
    # TODO: Create sprite for player
    # TODO: Add events to change sprite image based on button presses
    # TODO: Turn this into an example also
    controller = Controller()
    player = sprite_data[len(sprite_data) - 1].sprite
    player.apply_trait(MoveWithController(60, 60, controller))


if utils.should_execute(__name__):
    utils.execute(setup)
