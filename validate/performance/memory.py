"""
This test stresses memory. It creates lots of sprites (most as children of
the root) and a single long chain of parent-child relationships which tests
the capability of microcontrollers to handle deeper hierarchies.

The aim of this performance test is to find the limits that the engine can
cope with on a small microcontroller; specifically an Adafruit EdgeBadge.
"""
import validate.utils as utils
from pmpge.game import Game
from validate import test_data

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

row_1: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 6, "red-8x8.png"),  # First sibling drawn first (on bottom)
    test_data.SpriteData(11, 8, "orange-8x8.png"),
    test_data.SpriteData(16, 6, "yellow-8x8.png"),
    test_data.SpriteData(21, 8, "green-8x8.png"),
    test_data.SpriteData(26, 6, "blue-8x8.png"),
    test_data.SpriteData(31, 8, "violet-8x8.png"),
    test_data.SpriteData(36, 6, "red-8x8.png"),
    test_data.SpriteData(41, 8, "orange-8x8.png"),
    test_data.SpriteData(46, 6, "yellow-8x8.png"),
    test_data.SpriteData(51, 8, "green-8x8.png"),
    test_data.SpriteData(56, 6, "blue-8x8.png"),
    test_data.SpriteData(61, 8, "violet-8x8.png"),
    test_data.SpriteData(66, 6, "red-8x8.png"),
    test_data.SpriteData(71, 8, "orange-8x8.png"),
    test_data.SpriteData(76, 6, "yellow-8x8.png"),
    test_data.SpriteData(81, 8, "green-8x8.png"),
    test_data.SpriteData(86, 6, "blue-8x8.png"),
    test_data.SpriteData(91, 8, "violet-8x8.png"),
    test_data.SpriteData(96, 6, "red-8x8.png"),
    test_data.SpriteData(101, 8, "orange-8x8.png"),
    test_data.SpriteData(106, 6, "yellow-8x8.png"),
    test_data.SpriteData(111, 8, "green-8x8.png"),
    test_data.SpriteData(116, 6, "blue-8x8.png"),
    test_data.SpriteData(121, 8, "violet-8x8.png"),  # Last sibling - drawn last (on top)
]

row_2: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 20, "red-8x8.png"),  # First sibling drawn first (on bottom)
    test_data.SpriteData(11, 22, "orange-8x8.png"),
    test_data.SpriteData(16, 20, "yellow-8x8.png"),
    test_data.SpriteData(21, 22, "green-8x8.png"),
    test_data.SpriteData(26, 20, "blue-8x8.png"),
    test_data.SpriteData(31, 22, "violet-8x8.png"),
    test_data.SpriteData(36, 20, "red-8x8.png"),
    test_data.SpriteData(41, 22, "orange-8x8.png"),
    test_data.SpriteData(46, 20, "yellow-8x8.png"),
    test_data.SpriteData(51, 22, "green-8x8.png"),
    test_data.SpriteData(56, 20, "blue-8x8.png"),
    test_data.SpriteData(61, 22, "violet-8x8.png"),
    test_data.SpriteData(66, 20, "red-8x8.png"),
    test_data.SpriteData(71, 22, "orange-8x8.png"),
    test_data.SpriteData(76, 20, "yellow-8x8.png"),
    test_data.SpriteData(81, 22, "green-8x8.png"),
    test_data.SpriteData(86, 20, "blue-8x8.png"),
    test_data.SpriteData(91, 22, "violet-8x8.png"),
    test_data.SpriteData(96, 20, "red-8x8.png"),
    test_data.SpriteData(101, 22, "orange-8x8.png"),
    test_data.SpriteData(106, 20, "yellow-8x8.png"),
    test_data.SpriteData(111, 22, "green-8x8.png"),
    test_data.SpriteData(116, 20, "blue-8x8.png"),
    test_data.SpriteData(121, 22, "violet-8x8.png"),  # Last sibling - drawn last (on top)
]

row_3: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 34, "red-8x8.png"),  # First sibling drawn first (on bottom)
    test_data.SpriteData(11, 36, "orange-8x8.png"),
    test_data.SpriteData(16, 34, "yellow-8x8.png"),
    test_data.SpriteData(21, 36, "green-8x8.png"),
    test_data.SpriteData(26, 34, "blue-8x8.png"),
    test_data.SpriteData(31, 36, "violet-8x8.png"),
    test_data.SpriteData(36, 34, "red-8x8.png"),
    test_data.SpriteData(41, 36, "orange-8x8.png"),
    test_data.SpriteData(46, 34, "yellow-8x8.png"),
    test_data.SpriteData(51, 36, "green-8x8.png"),
    test_data.SpriteData(56, 34, "blue-8x8.png"),
    test_data.SpriteData(61, 36, "violet-8x8.png"),
    test_data.SpriteData(66, 34, "red-8x8.png"),
    test_data.SpriteData(71, 36, "orange-8x8.png"),
    test_data.SpriteData(76, 34, "yellow-8x8.png"),
    test_data.SpriteData(81, 36, "green-8x8.png"),
    test_data.SpriteData(86, 34, "blue-8x8.png"),
    test_data.SpriteData(91, 36, "violet-8x8.png"),
    test_data.SpriteData(96, 34, "red-8x8.png"),
    test_data.SpriteData(101, 36, "orange-8x8.png"),
    test_data.SpriteData(106, 34, "yellow-8x8.png"),
    test_data.SpriteData(111, 36, "green-8x8.png"),
    test_data.SpriteData(116, 34, "blue-8x8.png"),
    test_data.SpriteData(121, 36, "violet-8x8.png"),  # Last sibling - drawn last (on top)
]

row_4: list[test_data.SpriteData] = [
    test_data.SpriteData(6, 48, "red-8x8.png"),  # First sibling drawn first (on bottom)
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
    test_data.SpriteData(91, 50, "violet-8x8.png"),
    test_data.SpriteData(96, 48, "red-8x8.png"),
    test_data.SpriteData(101, 50, "orange-8x8.png"),
    test_data.SpriteData(106, 48, "yellow-8x8.png"),
    test_data.SpriteData(111, 50, "green-8x8.png"),
    test_data.SpriteData(116, 48, "blue-8x8.png"),
    test_data.SpriteData(121, 50, "violet-8x8.png"),  # Last sibling - drawn last (on top)
]

oom_recursion_check: list[test_data.SpriteData] = [
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
    # test_data.SpriteData(76, 92, "yellow-8x8.png"),
    # test_data.SpriteData(81, 94, "green-8x8.png"),
    # test_data.SpriteData(86, 92, "blue-8x8.png"),
    # test_data.SpriteData(91, 94, "violet-8x8.png"),
    test_data.SpriteData(96, 92, "red-8x8.png"),
    test_data.SpriteData(101, 94, "orange-8x8.png"),
    test_data.SpriteData(106, 92, "yellow-8x8.png"),
    test_data.SpriteData(111, 94, "green-8x8.png"),
    test_data.SpriteData(116, 92, "blue-8x8.png"),
    test_data.SpriteData(121, 94, "violet-8x8.png"),  # Leaf most - drawn last (on top)
]


def setup(game: Game):
    game.background_colour = (0, 0, 0)  # Black

    test_data.create_sprites(game, row_1, add_to_root=True)
    test_data.create_sprites(game, row_2, add_to_root=True)
    test_data.create_sprites(game, row_3, add_to_root=True)
    # test_data.create_sprites(game, row_4, add_to_root=True)

    test_data.create_sprites(game, oom_recursion_check, add_to_root=False)
    last = len(oom_recursion_check) - 1
    game.root.add_child(oom_recursion_check[0].sprite)
    for i in range(last):
        oom_recursion_check[i].sprite.add_child(oom_recursion_check[i + 1].sprite)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
