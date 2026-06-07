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
import validate.utils as utils
from pmpge.game import Game
from pmpge.graphics import game_object_hierarchy_changed
from validate import test_data

sprite_data_row_1: list[test_data.SpriteData] = [
    test_data.SpriteData(65, 15, "alien_c.png"),
    test_data.SpriteData(50, 15, "alien.png"),
    test_data.SpriteData(35, 15, "alien_c.png"),
    test_data.SpriteData(20, 15, "alien.png"),
]

sprite_data_row_2: list[test_data.SpriteData] = [
    test_data.SpriteData(140, 45, "alien_e.png"),
    test_data.SpriteData(110, 45, "alien_d.png"),
    test_data.SpriteData(80, 45, "alien_c.png"),
    test_data.SpriteData(50, 45, "alien_b.png"),
    test_data.SpriteData(20, 45, "alien.png"),
]

sprite_data_row_3: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 75, "alien_e.png"),
    test_data.SpriteData(50, 75, "alien_d.png"),
    test_data.SpriteData(80, 75, "alien_c.png"),
    test_data.SpriteData(110, 75, "alien_b.png"),
    test_data.SpriteData(140, 75, "alien.png"),
]

sprite_data_row_4: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 105, "alien_e.png"),
    test_data.SpriteData(50, 105, "alien_d.png"),
    test_data.SpriteData(80, 105, "alien_c.png"),
    test_data.SpriteData(110, 105, "alien_b.png"),
    test_data.SpriteData(140, 105, "alien.png"),
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

    test_data.create_sprites(game, sprite_data_row_1, add_to_root=False)
    game.root.add_child(sprite_data_row_1[3].sprite)
    sprite_data_row_1[3].sprite.add_child(sprite_data_row_1[2].sprite)
    sprite_data_row_1[2].sprite.add_child(sprite_data_row_1[1].sprite)
    sprite_data_row_1[1].sprite.add_child(sprite_data_row_1[0].sprite)

    test_data.create_sprites(game, sprite_data_row_2, add_to_root=False)
    game.root.add_child(sprite_data_row_2[4].sprite)
    sprite_data_row_2[4].sprite.add_child(sprite_data_row_2[3].sprite)
    sprite_data_row_2[3].sprite.add_child(sprite_data_row_2[2].sprite)
    sprite_data_row_2[2].sprite.add_child(sprite_data_row_2[1].sprite)
    sprite_data_row_2[1].sprite.add_child(sprite_data_row_2[0].sprite)
    utils.add_update_method(game, alternate_activated, fps=3)

    test_data.create_sprites(game, sprite_data_row_3, add_to_root=False)
    game.root.add_child(sprite_data_row_3[0].sprite)
    utils.add_update_method(game, add_children, fps=3)

    test_data.create_sprites(game, sprite_data_row_4, add_to_root=False)
    game.root.add_child(sprite_data_row_4[0].sprite)
    sprite_data_row_4[0].sprite.add_child(sprite_data_row_4[1].sprite)
    sprite_data_row_4[1].sprite.add_child(sprite_data_row_4[2].sprite)
    sprite_data_row_4[2].sprite.add_child(sprite_data_row_4[3].sprite)
    sprite_data_row_4[3].sprite.add_child(sprite_data_row_4[4].sprite)
    utils.add_update_method(game, destroy_children, fps=3)


if utils.should_execute(__name__):
    utils.execute(setup)
