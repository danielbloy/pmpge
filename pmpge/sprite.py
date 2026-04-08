from pmpge.game_object import GameObject
from pmpge.traits.position import Position


class Sprite(GameObject, Position):
    # TODO: Test this class
    # TODO: Document this clas
    def __init__(self, x: float, y: float, *traits, **kwargs):
        super().__init__(*traits, **kwargs)
        Position.__init__(self, x, y)
