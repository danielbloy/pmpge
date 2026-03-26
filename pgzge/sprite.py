from pgzge.core import GameObject
from pgzge.core import new_object_with_traits
from pgzge.traits.position import Position


# TODO: Add size, width, height, topleft, topright etc. properties
# TODO: Add bounding box property

class Sprite(GameObject, Position):
    def __init__(self, x: float, y: float, *traits, **kwargs):
        super().__init__(**kwargs)
        Position.__init__(self, x, y)

        for trait in traits:
            self.add_trait(trait)

    @staticmethod
    def new(x: float, y: float, *traits, kind: type = None, **kwargs) -> GameObject:
        base = GameObject(**kwargs)
        return new_object_with_traits(base, Position(x, y), *traits, kind=kind)
