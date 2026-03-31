from dataclasses import dataclass

from pgzge.controller import Controller


@dataclass
class MoveWithController:
    vx: int
    vy: int
    controller: Controller

    def update(self, dt: float):
        new_x, new_y = self.pos
        controller = self.controller

        if controller.left:
            new_x = new_x - (self.vx * dt)
        elif controller.right:
            new_x = new_x + (self.vx * dt)

        if controller.level > 0:
            if controller.up:
                new_y = new_y - (self.vy * dt)
            elif controller.down:
                new_y = new_y + (self.vy * dt)

        self.position = new_x, new_y
