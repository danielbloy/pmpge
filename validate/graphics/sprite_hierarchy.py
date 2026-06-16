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
from pmpge.utilities import add_rate_limited_func
from validate import test_data

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

sprite_data_row_1: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 6, "red-8x8.png"),
    test_data.SpriteData(8, 7, "orange-8x8.png"),
    test_data.SpriteData(10, 8, "yellow-8x8.png"),
    test_data.SpriteData(12, 9, "green-8x8.png"),
    test_data.SpriteData(14, 10, "blue-8x8.png"),
    test_data.SpriteData(16, 11, "violet-8x8.png"),
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


def rebuild_graphics_hierarchy(_: float):
    game_object_hierarchy_changed()


def alternate_activated(_: float):
    sprite_data_row_2[2].sprite.active = not sprite_data_row_2[2].sprite.active


add_index = 0


def add_children(_: float):
    global add_index

    if add_index >= len(sprite_data_row_3) - 1:
        return

    sprite_data_row_3[add_index].sprite.add_child(sprite_data_row_3[add_index + 1].sprite)
    add_index += 1


destroy_index = len(sprite_data_row_4) - 1


def destroy_children(_: float):
    global destroy_index

    if destroy_index < 0:
        return

    sprite_data_row_4[destroy_index].sprite.destroy()
    destroy_index -= 1


def setup(game: Game):
    game.background_colour = (0, 0, 0)  # Black
    add_rate_limited_func(game, rebuild_graphics_hierarchy, rate=1)

    test_data.create_sprites(game, sprite_data_row_1, add_to_root=False)
    last = len(sprite_data_row_1) - 1
    game.root.add_child(sprite_data_row_1[last].sprite)
    for i in range(last, 0, -1):
        sprite_data_row_1[i].sprite.add_child(sprite_data_row_1[i - 1].sprite)

    test_data.create_sprites(game, sprite_data_row_2, add_to_root=False)
    game.root.add_child(sprite_data_row_2[4].sprite)
    sprite_data_row_2[4].sprite.add_child(sprite_data_row_2[3].sprite)
    sprite_data_row_2[3].sprite.add_child(sprite_data_row_2[2].sprite)
    sprite_data_row_2[2].sprite.add_child(sprite_data_row_2[1].sprite)
    sprite_data_row_2[1].sprite.add_child(sprite_data_row_2[0].sprite)
    add_rate_limited_func(game, alternate_activated, rate=1)

    test_data.create_sprites(game, sprite_data_row_3, add_to_root=False)
    game.root.add_child(sprite_data_row_3[0].sprite)
    add_rate_limited_func(game, add_children, rate=1)

    test_data.create_sprites(game, sprite_data_row_4, add_to_root=False)
    game.root.add_child(sprite_data_row_4[0].sprite)
    sprite_data_row_4[0].sprite.add_child(sprite_data_row_4[1].sprite)
    sprite_data_row_4[1].sprite.add_child(sprite_data_row_4[2].sprite)
    sprite_data_row_4[2].sprite.add_child(sprite_data_row_4[3].sprite)
    sprite_data_row_4[3].sprite.add_child(sprite_data_row_4[4].sprite)
    add_rate_limited_func(game, destroy_children, rate=1)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
