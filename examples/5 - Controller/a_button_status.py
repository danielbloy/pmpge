"""
This example tracks the status of the controller buttons.
"""

import time

from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import Position

game: Game = Game(160, 120, (0, 0, 0))


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


game.add_update_func(terminate)

button_objects = [
    GameObject(Position(10, 110), DrawImage("start.png")),
    GameObject(Position(20, 110), DrawImage("select.png")),
    GameObject(Position(30, 110), DrawImage("l.png")),
    GameObject(Position(40, 110), DrawImage("r.png")),
    GameObject(Position(50, 110), DrawImage("u.png")),
    GameObject(Position(60, 110), DrawImage("d.png")),
    GameObject(Position(70, 110), DrawImage("a.png")),
    GameObject(Position(80, 110), DrawImage("b.png")),
    GameObject(Position(90, 110), DrawImage("x.png")),
    GameObject(Position(100, 110), DrawImage("y.png")),
    GameObject(Position(110, 110), DrawImage("ls.png")),
    GameObject(Position(120, 110), DrawImage("rs.png")),
]
for go in button_objects:
    game.add_child(go)


# Update the visibility of the buttons based on the controller values.
def update_buttons(dt: float):
    for i in range(12):
        button_objects[i].visible = Controller.values[i]


game.add_update_func(update_buttons)

finish = time.monotonic() + 5
game.run()
