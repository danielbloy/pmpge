import math


class Position:
    """
    Position is a specific location in 2D space, represented by an x and y co-ordinate.
    A Position can be inside the viewable display area of the game or outside of it.
    """

    x: float
    y: float

    def __init__(self, x, y: float):
        self.x: float = x
        self.y: float = y


class RelativeToParent:
    """
    RelativeToParent keeps the position of a GameObject a specified number of pixels
    horizontally and vertically relative to its parent GameObject. If the parent moves,
    the child will move with it at a constant offset. If the GameObject has no parent,
    the offset will be relative to the top left corner of the screen.

    RelativeToParent will not work unless added to a GameObject as it requires the
    parent property to be present.
    """

    parent: Position
    x: float
    y: float
    offset_x: int
    offset_y: int

    def __init__(self, offset_x, offset_y: int):
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y

    def update(self, dt: int):
        parent = self.parent
        if parent:
            self.x = parent.x + self.offset_x
            self.y = parent.y + self.offset_y
        else:
            self.x = self.offset_x
            self.y = self.offset_y


class AngularMotion:
    """
    This trait will rotate a sprite around a center position (cx, cy) with a given radius
    and angular_motion (specified in radians). This will blat any (x, y) coordinate pair
    so will not play nicely with other traits that set position.
    TODO: Test
    """
    x: float
    y: float
    cx: int
    cy: int
    radius: int
    angular_velocity: float  # This should be in radians
    angle: float

    def __init__(self, cx: int, cy: int, radius: int, angular_velocity: float, start_angle: float = 0.0):
        self.cx: int = cx
        self.cy: int = cy
        self.radius: int = radius
        self.angular_velocity: float = angular_velocity
        self.angle: float = start_angle

    def update(self, dt: float):
        angle = self.angle + (dt * self.angular_velocity)
        self.angle = angle

        radius = self.radius
        self.x = self.cx + (radius * math.cos(angle))
        self.y = self.cy + (radius * math.sin(angle))


class AngularRelativeToParent:
    """
    This is a specialisation of Relative to parent that is used with AngularMotion
    to orbit a parent. It simply sets (cx, cy) to the parents (x, y) as it moves.
    TODO: Test
    """
    parent: Position
    cx: int
    cy: int

    def update(self, dt: int):
        parent = self.parent
        if parent:
            self.cx = int(parent.x)
            self.cy = int(parent.y)


class FollowSprite:
    """
    This trait makes a sprite follow another sprite as the desired velocity.
    TODO: Test
    """
    sprite: Position
    x: float
    y: float
    vx: int
    vy: int

    def __init__(self, sprite: Position, vx, vy: int):
        self.sprite: Position = sprite
        self.vx: int = vx
        self.vy: int = vy

    def update(self, dt: float):
        sprite = self.sprite
        sx = sprite.x
        sy = sprite.y
        x = self.x
        y = self.y

        if sx < x:
            self.x = x - (dt * self.vx)
        elif sx > x:
            self.x = x + (dt * self.vx)

        if sy < y:
            self.y = y - (dt * self.vy)
        elif sy > y:
            self.y = y + (dt * self.vy)


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
