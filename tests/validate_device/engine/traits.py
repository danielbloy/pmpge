"""
Creates a hierarchy GameObjects with various Traits to see memory usage and
performance impact.
"""
import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.traits.lifetime import Lifetime
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position, StayInBounds, RelativeToParent


def setup(game: Game):
    for i in range(10):
        parent = GameObject(
            Position(i * 8, i * 2),
            Velocity(1 * 2, i * 5),
            StayInBounds(0, 0, 160, 120),
            Lifetime(i * 3)
        )
        game.add_child(parent)
        for _ in range(3):
            child = GameObject(
                Position(0, 0),
                RelativeToParent(i * 2, i * 4),
                Lifetime(i * 2),
                parent=parent
            )
            parent.add_child(child)
            for _ in range(2):
                grandchild = GameObject(
                    Position(0, 0),
                    RelativeToParent(i * -4, i * -8),
                    Lifetime(i),
                    parent=child
                )
                child.add_child(grandchild)


if utils.should_execute(__name__):
    utils.execute(setup)
