"""
Creates several rows of sprites (parents to the left, children to the right) to check the
z-order drawing works:

* Row 5: Siblings. This is a straight forward group of siblings to check the draw order.
  Red (left most) should be on the bottom, purple (right most) should be on the top.
* Row 2: Sprites are created parent first and added to the hierarchy parent first.
  If the parents are displayed on top of the children then the z-order does not work.
  Red (left most) should be on the bottom, purple (right most) should be on the top.
* Row 3: Sprites are created child first and added to the hierarchy parent first.
  If the parents are displayed on top of the children then the z-order does not work.
  Red (left most) should be on the bottom, purple (right most) should be on the top.
* Row 4: This row is partially created at start-up and then later extra children
  are added.
* Row 5: This row is completely created at start-up and then later the children
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

siblings: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 6, "red-8x8.png"),  # First sibling drawn first (on bottom)
    test_data.SpriteData(11, 8, "orange-8x8.png"),
    test_data.SpriteData(16, 6, "yellow-8x8.png"),
    test_data.SpriteData(21, 8, "green-8x8.png"),
    test_data.SpriteData(26, 6, "blue-8x8.png"),
    test_data.SpriteData(31, 8, "violet-8x8.png"),  # Last sibling - drawn last (on top)
]

create_parent_first_add_parent_first: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 20, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 22, "orange-8x8.png"),
    test_data.SpriteData(16, 20, "yellow-8x8.png"),
    test_data.SpriteData(21, 22, "green-8x8.png"),
    test_data.SpriteData(26, 20, "blue-8x8.png"),
    test_data.SpriteData(31, 22, "violet-8x8.png"),  # Leaf most - drawn last (on top)
]

create_child_first_add_parent_first: list[test_data.SpriteData] = [
    test_data.SpriteData(31, 36, "violet-8x8.png"),  # Leaf most - drawn last (on top)
    test_data.SpriteData(26, 34, "blue-8x8.png"),
    test_data.SpriteData(21, 36, "green-8x8.png"),
    test_data.SpriteData(16, 34, "yellow-8x8.png"),
    test_data.SpriteData(11, 36, "orange-8x8.png"),
    test_data.SpriteData(6, 34, "red-8x8.png"),  # Root most - drawn first (on bottom)
]

add_children_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 48, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 50, "orange-8x8.png"),
    test_data.SpriteData(16, 48, "yellow-8x8.png"),
    test_data.SpriteData(21, 50, "green-8x8.png"),
    test_data.SpriteData(26, 48, "blue-8x8.png"),
    test_data.SpriteData(31, 50, "violet-8x8.png"),
    test_data.SpriteData(36, 48, "red-8x8.png"),
    test_data.SpriteData(41, 50, "orange-8x8.png"),
    test_data.SpriteData(46, 48, "yellow-8x8.png"),
    test_data.SpriteData(51, 50, "green-8x8.png"),
    test_data.SpriteData(56, 48, "blue-8x8.png"),
    test_data.SpriteData(61, 50, "violet-8x8.png"),
    test_data.SpriteData(66, 48, "red-8x8.png"),
    test_data.SpriteData(71, 50, "orange-8x8.png"),
    test_data.SpriteData(76, 48, "yellow-8x8.png"),
    test_data.SpriteData(81, 50, "green-8x8.png"),
    test_data.SpriteData(86, 48, "blue-8x8.png"),
    test_data.SpriteData(91, 59, "violet-8x8.png"),  # Leaf most - drawn last (on top)
]

remove_children_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 62, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 64, "orange-8x8.png"),
    test_data.SpriteData(16, 62, "yellow-8x8.png"),
    test_data.SpriteData(21, 64, "green-8x8.png"),
    test_data.SpriteData(26, 62, "blue-8x8.png"),
    test_data.SpriteData(31, 64, "violet-8x8.png"),
    test_data.SpriteData(36, 62, "red-8x8.png"),
    test_data.SpriteData(41, 64, "orange-8x8.png"),
    test_data.SpriteData(46, 62, "yellow-8x8.png"),
    test_data.SpriteData(51, 64, "green-8x8.png"),
    test_data.SpriteData(56, 62, "blue-8x8.png"),
    test_data.SpriteData(61, 64, "violet-8x8.png"),
    test_data.SpriteData(66, 62, "red-8x8.png"),
    test_data.SpriteData(71, 64, "orange-8x8.png"),
    test_data.SpriteData(76, 62, "yellow-8x8.png"),
    test_data.SpriteData(81, 64, "green-8x8.png"),
    test_data.SpriteData(86, 62, "blue-8x8.png"),
    test_data.SpriteData(91, 64, "violet-8x8.png"),  # Leaf most - drawn last (on top)
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

    # Create some siblings to check they draw correctly.
    test_data.create_sprites(game, siblings, add_to_root=True)

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

    # The hierarchy for this set of sprites grows over time,
    add_rate_limited_func(game, add_children, rate=1)
    test_data.create_sprites(game, add_children_over_time, add_to_root=False)
    game.root.add_child(add_children_over_time[0].sprite)

    # The hierarchy for this set of sprites shrinks over time,
    add_rate_limited_func(game, destroy_children, rate=1)
    test_data.create_sprites(game, remove_children_over_time, add_to_root=False)
    last = len(remove_children_over_time) - 1
    game.root.add_child(remove_children_over_time[0].sprite)
    for i in range(last):
        remove_children_over_time[i].sprite.add_child(remove_children_over_time[i + 1].sprite)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
