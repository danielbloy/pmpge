from pmpge.game_object import GameObject
from pmpge.traits.position import Position


class Sprite(GameObject, Position):
    """
    A Sprite is a GameObject with a Position trait. The position of a Sprite is the
    center of the Sprite's image and bounding box if it has one. If a sprite has an
    image of 15 pixels by 15 pixels, the position of the Sprite will be the 8th pixel
    from the left and 8th pixel from the top.
    """

    # TODO: Test this class

    def __init__(self, x: float, y: float, *traits, **kwargs):
        super().__init__(*traits, **kwargs)
        Position.__init__(self, x, y)
