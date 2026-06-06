"""
Creates sprite in the center of the screen and allows the controller
to move it around. The other buttons toggle the visibility of sprites.
"""

import tests.validate_device.utils as utils
from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.traits.controller import MoveWithController
from pmpge.traits.position import StayInBounds

# The first 12 sprites represent the buttons which have their visibility
# switched as the buttons are preseed. The 13th sprite is the one moved
# around by the controller.
sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(10, 110, "start.png"),
    utils.SpriteData(20, 110, "select.png"),
    utils.SpriteData(30, 110, "l.png"),
    utils.SpriteData(40, 110, "r.png"),
    utils.SpriteData(50, 110, "u.png"),
    utils.SpriteData(60, 110, "d.png"),
    utils.SpriteData(70, 110, "a.png"),
    utils.SpriteData(80, 110, "b.png"),
    utils.SpriteData(90, 110, "x.png"),
    utils.SpriteData(100, 110, "y.png"),
    utils.SpriteData(110, 110, "ls.png"),
    utils.SpriteData(120, 110, "rs.png"),
    utils.SpriteData(80, 60, "hero_front.png", vx=0, vy=0),
]

index = 0
count = len(sprite_data)


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.create_sprites(game, sprite_data)
    controller = Controller()
    player = sprite_data[len(sprite_data) - 1].sprite
    player.apply_trait(MoveWithController(controller, 60, 60))
    player.apply_trait(StayInBounds(8, 8, game.width - 8, game.height - 8))

    # Update the visibility of the buttons based on the controller values.
    def update_buttons(dt: float):
        for i in range(12):
            sprite_data[i].sprite.visible = Controller.values[i]

    game.add_update_func(update_buttons)


if utils.should_execute(__name__):
    utils.execute(setup)
