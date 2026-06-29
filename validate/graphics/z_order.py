"""
Creates several rows of sprites (parents to the left, children to the right) to check the
z-order drawing works:

* Row 1: Sibling chain
* Row 2: Parent child chain
* Row 3: Parent child chain - alternative add
* Row 4: Sibling, parent and child chain (2d)
* Row 5: Parent child chain - growing
* Row 6: Parent child chain - shrinking

This also tests the game_object_hierarchy_changed() function which executes once per
second. On a microcontroller with a screen connected via SPI, this will likely cause
the screen to flicker once per second due to the update.

Detail of tests:

Row 1
Siblings. This is a straight forward group of siblings to check the draw order.
Red (left most) should be on the bottom, purple (right most) should be on the top.

Row 2
Sprites are created parent first and added to the hierarchy parent first.
If the parents are displayed on top of the children then the z-order does not work.
Red (left most) should be on the bottom, purple (right most) should be on the top.

Row 3
Sprites are created child first and added to the hierarchy parent first.
If the parents are displayed on top of the children then the z-order does not work.
Red (left most) should be on the bottom, purple (right most) should be on the top.

Row 4a
This is designed to demonstrate the full z order with siblings, children and
grandchildren. Each "column" of sprites is at the same "level" in the hierarchy (
parent, child or grandchild). The leftmost column should be at the bottom and the
rightmost column at the top.

Row 4b
This tests that z-order is not affected when a sprites image is changed. This is
a test specifically designed to validate how images are reloaded in graphics
drivers such as the displayio driver.

Row 5
This row is partially created at start-up and then later extra children are added.

Row 6
This row is completely created at start-up and then later the children are destroyed.
"""
import validate.utils as utils
from pmpge.game import Game
from pmpge.graphics import game_object_hierarchy_changed
from pmpge.utilities import add_rate_limited_func
from validate import test_data

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

# Row 1
siblings: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 6, "red-8x8.png"),  # First sibling drawn first (on bottom)
    test_data.SpriteData(11, 8, "orange-8x8.png"),
    test_data.SpriteData(16, 6, "yellow-8x8.png"),
    test_data.SpriteData(21, 8, "green-8x8.png"),
    test_data.SpriteData(26, 6, "blue-8x8.png"),
    test_data.SpriteData(31, 8, "violet-8x8.png"),  # Last sibling - drawn last (on top)
]

# Row 2
create_parent_first_add_parent_first: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 20, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 22, "orange-8x8.png"),
    test_data.SpriteData(16, 20, "yellow-8x8.png"),
    test_data.SpriteData(21, 22, "green-8x8.png"),
    test_data.SpriteData(26, 20, "blue-8x8.png"),
    test_data.SpriteData(31, 22, "violet-8x8.png"),  # Leaf most - drawn last (on top)
]

# Row 3
create_child_first_add_parent_first: list[test_data.SpriteData] = [
    test_data.SpriteData(31, 36, "violet-8x8.png"),  # Leaf most - drawn last (on top)
    test_data.SpriteData(26, 34, "blue-8x8.png"),
    test_data.SpriteData(21, 36, "green-8x8.png"),
    test_data.SpriteData(16, 34, "yellow-8x8.png"),
    test_data.SpriteData(11, 36, "orange-8x8.png"),
    test_data.SpriteData(6, 34, "red-8x8.png"),  # Root most - drawn first (on bottom)
]

# Row 4a
full_tree_parents: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 48, "red-8x8.png"),  # Parent 1
    test_data.SpriteData(8, 54, "orange-8x8.png"),  # Parent 2
    test_data.SpriteData(6, 60, "red-8x8.png"),  # Parent 3
    test_data.SpriteData(8, 66, "orange-8x8.png"),  # Parent 4
]

full_tree_children: list[test_data.SpriteData] = [
    test_data.SpriteData(12, 47, "yellow-8x8.png"),  # Parent 1 - Child 1
    test_data.SpriteData(14, 51, "green-8x8.png"),  # Parent 1 - Child 2
    test_data.SpriteData(12, 55, "blue-8x8.png"),  # Parent 1 - Child 3
    test_data.SpriteData(14, 59, "yellow-8x8.png"),  # Parent 3 - Child 4
    test_data.SpriteData(12, 63, "green-8x8.png"),  # Parent 3 - Child 5
    test_data.SpriteData(14, 67, "blue-8x8.png"),  # Parent 3 - Child 6
]

full_tree_grandchildren: list[test_data.SpriteData] = [
    test_data.SpriteData(18, 48, "red-8x8.png"),  # Child 2 - Grandchild 1
    test_data.SpriteData(20, 54, "orange-8x8.png"),  # Child 2 - Grandchild 2
    test_data.SpriteData(18, 60, "red-8x8.png"),  # Child 5 - Grandchild 3
    test_data.SpriteData(20, 66, "orange-8x8.png"),  # Child 5 - Grandchild 4
]

# Row 4b
change_image_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(41, 48, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(46, 50, "orange-8x8.png"),
    test_data.SpriteData(51, 48, "yellow-8x8.png"),
    test_data.SpriteData(56, 50, "green-8x8.png"),  # Leaf most - drawn last (on top)
]

# Row 5
add_children_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 78, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 80, "orange-8x8.png"),
    test_data.SpriteData(16, 78, "yellow-8x8.png"),
    test_data.SpriteData(21, 80, "green-8x8.png"),
    test_data.SpriteData(26, 78, "blue-8x8.png"),
    test_data.SpriteData(31, 80, "violet-8x8.png"),
    test_data.SpriteData(36, 78, "red-8x8.png"),
    test_data.SpriteData(41, 80, "orange-8x8.png"),
    test_data.SpriteData(46, 78, "yellow-8x8.png"),
    test_data.SpriteData(51, 80, "green-8x8.png"),
    test_data.SpriteData(56, 78, "blue-8x8.png"),
    test_data.SpriteData(61, 80, "violet-8x8.png"),
    test_data.SpriteData(66, 78, "red-8x8.png"),
    test_data.SpriteData(71, 80, "orange-8x8.png"),
    test_data.SpriteData(76, 78, "yellow-8x8.png"),
    test_data.SpriteData(81, 80, "green-8x8.png"),
    test_data.SpriteData(86, 78, "blue-8x8.png"),
    test_data.SpriteData(91, 80, "violet-8x8.png"),  # Leaf most - drawn last (on top)
]

# Row 6
destroy_children_over_time: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 92, "red-8x8.png"),  # Root most - drawn first (on bottom)
    test_data.SpriteData(11, 94, "orange-8x8.png"),
    test_data.SpriteData(16, 92, "yellow-8x8.png"),
    test_data.SpriteData(21, 94, "green-8x8.png"),
    test_data.SpriteData(26, 92, "blue-8x8.png"),
    test_data.SpriteData(31, 94, "violet-8x8.png"),
    test_data.SpriteData(36, 92, "red-8x8.png"),
    test_data.SpriteData(41, 94, "orange-8x8.png"),
    test_data.SpriteData(46, 92, "yellow-8x8.png"),
    test_data.SpriteData(51, 94, "green-8x8.png"),
    test_data.SpriteData(56, 92, "blue-8x8.png"),
    test_data.SpriteData(61, 94, "violet-8x8.png"),
    test_data.SpriteData(66, 92, "red-8x8.png"),
    test_data.SpriteData(71, 94, "orange-8x8.png"),
    test_data.SpriteData(76, 92, "yellow-8x8.png"),
    test_data.SpriteData(81, 94, "green-8x8.png"),
    test_data.SpriteData(86, 92, "blue-8x8.png"),
    test_data.SpriteData(91, 94, "violet-8x8.png"),  # Leaf most - drawn last (on top)
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


destroy_index = len(destroy_children_over_time) - 1


def destroy_children(_: float):
    global destroy_index

    if destroy_index < 0:
        return

    destroy_children_over_time[destroy_index].sprite.destroy()
    destroy_index -= 1


change_image_index: int = 0


def change_image(_: float):
    global change_image_index
    change_image_index += 1
    images = ["red-8x8.png", "blue-8x8.png"]
    change_image_index = change_image_index % len(images)
    change_image_over_time[0].sprite.image.name = images[change_image_index]


def setup(game: Game):
    game.background_colour = (0, 0, 0)  # Black
    add_rate_limited_func(game, rebuild_graphics_hierarchy, rate=1)

    # Row 1: Create some siblings to check they draw correctly.
    test_data.create_sprites(game, siblings, add_to_root=True)

    # Row 2: The list contains the parent first, leaf most last. We add them in parent order (forward).
    test_data.create_sprites(game, create_parent_first_add_parent_first, add_to_root=False)
    last = len(create_parent_first_add_parent_first) - 1
    game.root.add_child(create_parent_first_add_parent_first[0].sprite)
    for i in range(last):
        create_parent_first_add_parent_first[i].sprite.add_child(create_parent_first_add_parent_first[i + 1].sprite)

    # Row 3: The list contains the leaf most first, parent last. We add them in parent order (reverse).
    test_data.create_sprites(game, create_child_first_add_parent_first, add_to_root=False)
    last = len(create_child_first_add_parent_first) - 1
    game.root.add_child(create_child_first_add_parent_first[last].sprite)
    for i in range(last, 0, -1):
        create_child_first_add_parent_first[i].sprite.add_child(create_child_first_add_parent_first[i - 1].sprite)

    # Row 4a: Create the full tree
    test_data.create_sprites(game, full_tree_parents, add_to_root=True)

    test_data.create_sprites(game, full_tree_children, add_to_root=False)
    for i, obj in enumerate(full_tree_children):
        parent = full_tree_parents[0 if 1 < 3 else 2]
        parent.sprite.add_child(obj.sprite)

    test_data.create_sprites(game, full_tree_grandchildren, add_to_root=False)
    for i, obj in enumerate(full_tree_grandchildren):
        parent = full_tree_children[1 if 1 < 2 else 4]
        parent.sprite.add_child(obj.sprite)

    # Row 4b: Alternates the parents colour to validate it does not affect z-order.
    test_data.create_sprites(game, change_image_over_time, add_to_root=False)
    last = len(change_image_over_time) - 1
    game.root.add_child(change_image_over_time[0].sprite)
    for i in range(last):
        change_image_over_time[i].sprite.add_child(change_image_over_time[i + 1].sprite)

    add_rate_limited_func(game, change_image, rate=2)

    # Row 5: The hierarchy for this set of sprites grows over time,
    add_rate_limited_func(game, add_children, rate=1)
    test_data.create_sprites(game, add_children_over_time, add_to_root=False)
    game.root.add_child(add_children_over_time[0].sprite)

    # Row 6: The hierarchy for this set of sprites shrinks over time,
    add_rate_limited_func(game, destroy_children, rate=1)
    test_data.create_sprites(game, destroy_children_over_time, add_to_root=False)
    last = len(destroy_children_over_time) - 1
    game.root.add_child(destroy_children_over_time[0].sprite)
    for i in range(last):
        destroy_children_over_time[i].sprite.add_child(destroy_children_over_time[i + 1].sprite)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
