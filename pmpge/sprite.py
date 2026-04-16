from pmpge.game_object import GameObject
from pmpge.traits.position import Position


class Sprite(GameObject, Position):
    """
    A Sprite is a GameObject with a Position trait. The position of a Sprite is the
    center of the Sprite's image and bounding box if it has one.

    If a sprite has an image of 15 pixels by 15 pixels, the position of the Sprite
    will be the 8th pixel from the left and 8th pixel from the top.

    If the size of the Sprite's image is an even number of pixels in either direction,
    the centre is offset one pixel to the right and one pixel down. For example, if
    a sprite has an image of 16 pixels by 16 pixels, the position of the Sprite
    will be the 9th pixel from the left and 9th pixel from the top. This leaves 7 pixels
    to the right and 7 pixels below the centre of the Sprite.
    """

    def __init__(self, x: float, y: float, *traits, **kwargs):
        super().__init__(*traits, **kwargs)
        Position.__init__(self, x, y)

    @property
    def position(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        self.x = position[0]
        self.y = position[1]

    @property
    def pos(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self.x = pos[0]
        self.y = pos[1]
