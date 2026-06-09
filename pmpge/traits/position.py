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


class BoundPosition:
    """
    BoundPosition keeps a GameObjects position within a specified range of x and y co-ordinates.
    The co-ordinates do not need to be entirely within the visible bounds of the screen.

    The BoundPosition trait requires a Position trait to be present on the GameObject.
    """

    x: float
    y: float
    bounds: tuple[int, int, int, int]

    def __init__(self, min_x, min_y, max_x, max_y: int):
        self.bounds = min_x, min_y, max_x, max_y

    def update(self, dt: float):
        min_x, min_y, max_x, max_y = self.bounds

        self.x = max(self.x, min_x)
        self.x = min(self.x, max_x)
        self.y = max(self.y, min_y)
        self.y = min(self.y, max_y)


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


class AngularRelativeToParent:
    """
    This is a specialisation of Relative to parent that is used with AngularMotion
    to orbit a parent. It simply sets (cx, cy) to the parents (x, y) as it moves.
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
    """
    target: Position
    x: float
    y: float
    vx: int
    vy: int

    def __init__(self, sprite: Position, vx, vy: int):
        self.target: Position = sprite
        self.vx: int = vx
        self.vy: int = vy

    def update(self, dt: float):
        sprite = self.target
        sx = sprite.x
        sy = sprite.y
        x = self.x
        y = self.y

        # Calculate delta
        dx = sx - x
        dy = sy - y

        # Calculate movement
        mx = (dt * abs(self.vx))
        my = (dt * abs(self.vy))

        # If the movement amount is greater than the delta, just move to target
        if mx > abs(dx):
            self.x = sx
        else:
            # Decide whether to go left or right
            if dx < 0:
                self.x = x - mx
            elif dx > 0:
                self.x = x + mx

        # If the movement amount is greater than the delta, just move to target
        if my > abs(dy):
            self.y = sy
        else:
            # Decide whether to go up or down
            if dy < 0:
                self.y = y - my
            elif dy > 0:
                self.y = y + my
