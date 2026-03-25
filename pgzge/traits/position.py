class Position:
    def __init__(self, x, y: float):
        self.x: float = x
        self.y: float = y

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y

    @position.setter
    def position(self, position: tuple[float, float]) -> None:
        self.x = position[0]
        self.y = position[1]

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, pos: tuple[float, float]) -> None:
        self.x = pos[0]
        self.y = pos[1]


class RelativeToParent:
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
