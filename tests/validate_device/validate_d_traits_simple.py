"""
Creates a set of GameObjects with various Traits in the normal forms
to validate it works.
"""
import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.traits.lifetime import Lifetime
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position, StayInBounds


def setup(game: Game):
    trait_as_class = GameObject(Position)
    game.add_child(trait_as_class)

    trait_as_instance = GameObject(Lifetime(10))
    game.add_child(trait_as_instance)

    two_traits = GameObject(
        Position,
        Velocity(20, 10)
    )
    game.add_child(two_traits)

    four_traits = GameObject(
        Position(100, 50),
        Velocity(20, 10),
        StayInBounds(0, 0, 160, 120),
        Lifetime(10)
    )
    game.add_child(four_traits)


if utils.should_execute(__name__):
    utils.execute(setup)
