from pmpge.sprite import Sprite


class Position:
    """
    Position is a specific location in 2D space, represented by an x and y co-ordinate.
    A Position can be inside the viewable display area of the game or outside of it.
    """

    x: float
    y: float

    # TODO: Test this class

    def __init__(self, x, y: float):
        self.x: float = x
        self.y: float = y

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


class RelativeToParent:
    """
    RelativeToParent keeps the position of a GameObject a specified number of pixels
    horizontally and vertically relative to its parent GameObject. If the parent moves,
    the child will move with it at a constant offset. If the GameObject has no parent,
    the offset will be relative to the top left corner of the screen.

    The RelativeToParent trait requires a Position trait to be present on the GameObject
    amd the parent GameObject.
    """

    parent: Sprite
    x: float
    y: float
    offset_x: int
    offset_y: int

    # TODO: Test this class

    def __init__(self, offset_x, offset_y: int):
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y

    def update(self, dt: int):
        if self.parent:
            self.x = self.parent.x + self.offset_x
            self.y = self.parent.y + self.offset_y
        else:
            self.x = self.offset_x
            self.y = self.offset_y


class StayInBounds:
    """
    StayInBounds keeps a GameObjects position within a specified range of x and y co-ordinates.
    The co-ordinates do not need to be entirely within the visible bounds of the screen.

    The StayInBounds trait requires a Position trait to be present on the GameObject.
    """

    x: float
    y: float
    min_x: int
    min_y: int
    max_x: int
    max_y: int

    # TODO: Test this class

    def __init__(self, min_x, min_y, max_x, max_y: int):
        self.min_x: int = min_x
        self.max_x: int = max_x
        self.min_y: int = min_y
        self.max_y: int = max_y

    def update(self, dt: float):
        if self.x < self.min_x:
            self.x = self.min_x
        elif self.x > self.max_x:
            self.x = self.max_x

        if self.y < self.min_y:
            self.y = self.min_y
        elif self.y > self.max_y:
            self.y = self.max_y
