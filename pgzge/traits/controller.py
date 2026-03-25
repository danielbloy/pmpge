from pgzero.keyboard import Keyboard


# TODO: Rename Controller1 and remove all dependencies on pygame
class MoveWithKeyboard:
    def __init__(self, vx, vy: int, keyboard: Keyboard):
        self.vx: int = vx
        self.vy: int = vy
        self.keyboard: Keyboard = keyboard

    def update(self, dt: float):
        new_pos = self.pos
        keyboard = self.keyboard
        if keyboard.a or keyboard.left:
            new_pos = (new_pos[0] - (self.vx * dt), new_pos[1])
        elif keyboard.d or keyboard.right:
            new_pos = (new_pos[0] + (self.vx * dt), new_pos[1])

        self.position = new_pos
