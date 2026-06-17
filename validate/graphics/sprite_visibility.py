"""
Creates sprites on the screen and adjusts visibility. There is a
row for each test.
* Row one contains 4 sprites attached to the root, cycling which sprite is
  invisible. When the end of the row is reached, it restarts.
* The second row alternates active mid-way through the hierarchy which should
  hide and show 3 of the 5 sprites. The three sprites that should flash are
  indicated by purple squares.
"""
import validate.utils as utils
from pmpge.game import Game
from pmpge.utilities import add_rate_limited_func
from validate import test_data

cycle_visibility_data: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 20, "alien.png"),
    test_data.SpriteData(60, 20, "alien.png"),
    test_data.SpriteData(100, 20, "alien.png"),
    test_data.SpriteData(140, 20, "alien.png"),
]

index = 0


def cycle_visibility(_: float):
    global index

    cycle_visibility_data[index].sprite.visible = True
    index = (index + 1) % len(cycle_visibility_data)
    cycle_visibility_data[index].sprite.visible = False


# Each of these objects is in a hierarchy, with the first object being the root
# and each subsequent object a child of the previous.
hierarchy: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 55, "alien_e.png"),
    test_data.SpriteData(50, 55, "alien_d.png"),
    test_data.SpriteData(80, 55, "alien_c.png"),
    test_data.SpriteData(110, 55, "alien_b.png"),
    test_data.SpriteData(140, 55, "alien.png"),
]

# These sprites are used to indicate which sprites should flash.
hierarchy_dots: list[test_data.SpriteData] = [
    test_data.SpriteData(80, 75, "violet-8x8.png"),
    test_data.SpriteData(110, 75, "violet-8x8.png"),
    test_data.SpriteData(140, 75, "violet-8x8.png"),
]


# Alternates the visibility of the middle sprite making the three right most
# sprites "flash".
def alternate_activated(_: float):
    hierarchy[2].sprite.active = not hierarchy[2].sprite.active


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange

    # Create the objects that we will cycle through
    test_data.create_sprites(game, cycle_visibility_data)
    add_rate_limited_func(game, cycle_visibility, rate=4)

    # Create the object hierarchy and switch the third object.
    test_data.create_sprites(game, hierarchy, add_to_root=False)
    test_data.create_sprites(game, hierarchy_dots, add_to_root=True)
    game.root.add_child(hierarchy[0].sprite)
    for i in range(len(hierarchy) - 1):
        hierarchy[i].sprite.add_child(hierarchy[i + 1].sprite)

    add_rate_limited_func(game, alternate_activated, rate=1)


if utils.should_execute(__name__):
    utils.execute(setup)
