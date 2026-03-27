from pgzge.core import GameObject
from pgzge.traits.position import Position


# TODO: Add size, width, height, topleft, topright etc. properties
# TODO: Add bounding box property

class Sprite(GameObject, Position):
    def __init__(self, x: float, y: float, *traits, **kwargs):
        super().__init__(*traits, **kwargs)
        Position.__init__(self, x, y)
