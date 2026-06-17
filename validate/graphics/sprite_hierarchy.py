"""
Creates three rows of sprites (parents to the left, children to the right)
to check the hierarchy works:
* The first row of sprites are created parent first and added to the hierarchy parent first.
  If the parents are displayed on top of the children then the z-order does not work.
  Red (left most) should be on the bottom, purple (right most) should be on the top.
* The second row of sprites are created child first and added to the hierarchy parent first.
  If the parents are displayed on top of the children then the z-order does not work.
  Red (left most) should be on the bottom, purple (right most) should be on the top.
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

create_parent_first_add_parent_first: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 6, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 8, "orange-8x8.png"),
    test_data.SpriteData(16, 6, "yellow-8x8.png"),
    test_data.SpriteData(21, 8, "green-8x8.png"),
    test_data.SpriteData(26, 6, "blue-8x8.png"),
    test_data.SpriteData(31, 8, "violet-8x8.png"),  # Leaf most - drawn last (on top)
]

create_child_first_add_parent_first: list[test_data.SpriteData] = [
    test_data.SpriteData(31, 32, "violet-8x8.png"),  # Leaf most - drawn last (on top)
    test_data.SpriteData(26, 30, "blue-8x8.png"),
    test_data.SpriteData(21, 32, "green-8x8.png"),
    test_data.SpriteData(16, 30, "yellow-8x8.png"),
    test_data.SpriteData(11, 32, "orange-8x8.png"),
    test_data.SpriteData(6, 30, "red-8x8.png"),  # Root most - drawn first (on bottom)
]

add_children_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 55, "alien_e.png"),
    test_data.SpriteData(50, 55, "alien_d.png"),
    test_data.SpriteData(80, 55, "alien_c.png"),
    test_data.SpriteData(110, 55, "alien_b.png"),
    test_data.SpriteData(140, 55, "alien.png"),
]

remove_children_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 85, "alien_e.png"),
    test_data.SpriteData(50, 85, "alien_d.png"),
    test_data.SpriteData(80, 85, "alien_c.png"),
    test_data.SpriteData(110, 85, "alien_b.png"),
    test_data.SpriteData(140, 85, "alien.png"),
]


def rebuild_graphics_hierarchy(_: float):
    game_object_hierarchy_changed()


add_index = 0


def add_children(_: float):
    global add_index

    if add_index >= len(add_children_over_time) - 1:
        return

    add_children_over_time[add_index].sprite.add_child(add_children_over_time[add_index + 1].sprite)
    add_index += 1


destroy_index = len(remove_children_over_time) - 1


def destroy_children(_: float):
    global destroy_index

    if destroy_index < 0:
        return

    remove_children_over_time[destroy_index].sprite.destroy()
    destroy_index -= 1


def setup(game: Game):
    game.background_colour = (0, 0, 0)  # Black
    add_rate_limited_func(game, rebuild_graphics_hierarchy, rate=1)

    # The list contains the parent first, leaf most last. We add them tin parent order (forward).
    test_data.create_sprites(game, create_parent_first_add_parent_first, add_to_root=False)
    last = len(create_parent_first_add_parent_first) - 1
    game.root.add_child(create_parent_first_add_parent_first[0].sprite)
    for i in range(last):
        create_parent_first_add_parent_first[i].sprite.add_child(create_parent_first_add_parent_first[i + 1].sprite)

    # The list contains the leaf most first, parent last. We add them in parent order (reverse).
    test_data.create_sprites(game, create_child_first_add_parent_first, add_to_root=False)
    last = len(create_child_first_add_parent_first) - 1
    game.root.add_child(create_child_first_add_parent_first[last].sprite)
    for i in range(last, 0, -1):
        create_child_first_add_parent_first[i].sprite.add_child(create_child_first_add_parent_first[i - 1].sprite)

    test_data.create_sprites(game, add_children_over_time, add_to_root=False)
    game.root.add_child(add_children_over_time[0].sprite)
    add_rate_limited_func(game, add_children, rate=1)

    test_data.create_sprites(game, remove_children_over_time, add_to_root=False)
    game.root.add_child(remove_children_over_time[0].sprite)
    remove_children_over_time[0].sprite.add_child(remove_children_over_time[1].sprite)
    remove_children_over_time[1].sprite.add_child(remove_children_over_time[2].sprite)
    remove_children_over_time[2].sprite.add_child(remove_children_over_time[3].sprite)
    remove_children_over_time[3].sprite.add_child(remove_children_over_time[4].sprite)
    add_rate_limited_func(game, destroy_children, rate=1)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
