"""
Creates three rows of sprites (parents to the left, children to the right)
to check the hierarchy works:
* The Top row are created child first but added parent first. If the
  parents are displayed on top of the children then the z-order does not work
* The second row alternates active mid-way through the hierarchy which should
  hide and show half the row.
* The third row is partially created at start-up and then later extra children
  are added.
* The fourth row is completely created at start-up and then later the children
  are destroyed.

This also tests the game_object_hierarchy_changed() function.
"""

import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.graphics import game_object_hierarchy_changed

sprite_data_row_1: list[utils.SpriteData] = [
    utils.SpriteData(65, 15, 0, 0, "alien_c.png"),
    utils.SpriteData(50, 15, 0, 0, "alien.png"),
    utils.SpriteData(35, 15, 0, 0, "alien_c.png"),
    utils.SpriteData(20, 15, 0, 0, "alien.png"),
]

sprite_data_row_2: list[utils.SpriteData] = [
    utils.SpriteData(140, 45, 0, 0, "alien_e.png"),
    utils.SpriteData(110, 45, 0, 0, "alien_d.png"),
    utils.SpriteData(80, 45, 0, 0, "alien_c.png"),
    utils.SpriteData(50, 45, 0, 0, "alien_b.png"),
    utils.SpriteData(20, 45, 0, 0, "alien.png"),
]

sprite_data_row_3: list[utils.SpriteData] = [
    utils.SpriteData(20, 75, 0, 0, "alien_e.png"),
    utils.SpriteData(50, 75, 0, 0, "alien_d.png"),
    utils.SpriteData(80, 75, 0, 0, "alien_c.png"),
    utils.SpriteData(110, 75, 0, 0, "alien_b.png"),
    utils.SpriteData(140, 75, 0, 0, "alien.png"),
]

sprite_data_row_4: list[utils.SpriteData] = [
    utils.SpriteData(20, 105, 0, 0, "alien_e.png"),
    utils.SpriteData(50, 105, 0, 0, "alien_d.png"),
    utils.SpriteData(80, 105, 0, 0, "alien_c.png"),
    utils.SpriteData(110, 105, 0, 0, "alien_b.png"),
    utils.SpriteData(140, 105, 0, 0, "alien.png"),
]


def rebuild_graphics_hierarchy(game: Game):
    game_object_hierarchy_changed()


def alternate_activated(game: Game):
    sprite_data_row_2[2].sprite.active = not sprite_data_row_2[2].sprite.active


add_index = 0


def add_children(game: Game):
    global add_index

    if add_index >= len(sprite_data_row_3) - 1:
        return

    sprite_data_row_3[add_index].sprite.add_child(sprite_data_row_3[add_index + 1].sprite)
    add_index += 1


destroy_index = len(sprite_data_row_4) - 1


def destroy_children(game: Game):
    global destroy_index

    if destroy_index < 0:
        return

    sprite_data_row_4[destroy_index].sprite.destroy()
    destroy_index -= 1


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.add_update_method(game, rebuild_graphics_hierarchy, fps=1)

    utils.create_sprites(game, sprite_data_row_1, add_to_root=False)
    game.root.add_child(sprite_data_row_1[3].sprite)
    sprite_data_row_1[3].sprite.add_child(sprite_data_row_1[2].sprite)
    sprite_data_row_1[2].sprite.add_child(sprite_data_row_1[1].sprite)
    sprite_data_row_1[1].sprite.add_child(sprite_data_row_1[0].sprite)

    utils.create_sprites(game, sprite_data_row_2, add_to_root=False)
    game.root.add_child(sprite_data_row_2[4].sprite)
    sprite_data_row_2[4].sprite.add_child(sprite_data_row_2[3].sprite)
    sprite_data_row_2[3].sprite.add_child(sprite_data_row_2[2].sprite)
    sprite_data_row_2[2].sprite.add_child(sprite_data_row_2[1].sprite)
    sprite_data_row_2[1].sprite.add_child(sprite_data_row_2[0].sprite)
    utils.add_update_method(game, alternate_activated, fps=3)

    utils.create_sprites(game, sprite_data_row_3, add_to_root=False)
    game.root.add_child(sprite_data_row_3[0].sprite)
    utils.add_update_method(game, add_children, fps=3)

    utils.create_sprites(game, sprite_data_row_4, add_to_root=False)
    game.root.add_child(sprite_data_row_4[0].sprite)
    sprite_data_row_4[0].sprite.add_child(sprite_data_row_4[1].sprite)
    sprite_data_row_4[1].sprite.add_child(sprite_data_row_4[2].sprite)
    sprite_data_row_4[2].sprite.add_child(sprite_data_row_4[3].sprite)
    sprite_data_row_4[3].sprite.add_child(sprite_data_row_4[4].sprite)
    utils.add_update_method(game, destroy_children, fps=3)


if utils.should_execute(__name__):
    utils.execute(setup)
