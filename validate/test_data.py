import math

from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.controller import MoveWithController
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import BoundVelocity
from pmpge.traits.physics import Velocity, Acceleration
from pmpge.traits.position import AngularMotion, AngularRelativeToParent, FollowSprite, StayInBounds
from pmpge.traits.position import HorizontalBounce, VerticalBounce
from pmpge.traits.position import HorizontalOscillator, VerticalOscillator


class SpriteData:
    """
    Used to hold data for creating Sprites with create_sprites().
    """
    x: int
    y: int
    vx: int | None
    vy: int | None
    ax: int | None
    ay: int | None
    image: str
    sprite: Sprite

    def __init__(self, x: int, y: int, image: str, vx=None, vy=None, ax=None, ay=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image = image
        self.ax = ax
        self.ay = ay


def create_sprites(game: Game, sprite_data: list[SpriteData], add_to_root: bool = True, include_graphics: bool = True):
    """
    utility method to create sprites and optionally add them to the root of the Game instance
    """
    for data in sprite_data:
        sprite = Sprite(data.x, data.y)

        if data.vx is not None and data.vy is not None:
            sprite.apply_trait(Velocity(data.vx, data.vy))

        if data.ax is not None and data.ay is not None:
            sprite.apply_trait(Acceleration(data.ax, data.ay))

        if include_graphics:
            sprite.apply_trait(DrawImage(data.image))

        data.sprite = sprite

        if add_to_root:
            game.add_child(sprite)


def create_controller_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created (13 sprites):
        - 12 sprites showing the status of each controller button
        - 1 hero sprite that can be moved around with the controller
    """
    # Now add a button for each controller button.
    row_1 = game.height - 4
    row_0 = row_1 - 8
    controller_sprites: list[SpriteData] = [
        SpriteData(4, row_0, "start.png"),
        SpriteData(12, row_0, "select.png"),
        SpriteData(20, row_0, "l.png"),
        SpriteData(28, row_0, "r.png"),
        SpriteData(36, row_0, "u.png"),
        SpriteData(44, row_0, "d.png"),
        SpriteData(4, row_1, "a.png"),
        SpriteData(12, row_1, "b.png"),
        SpriteData(20, row_1, "x.png"),
        SpriteData(28, row_1, "y.png"),
        SpriteData(36, row_1, "ls.png"),
        SpriteData(44, row_1, "rs.png"),
    ]
    create_sprites(game, controller_sprites, include_graphics=include_graphics)

    # Update the visibility of the buttons based on the controller values.
    def update_buttons(dt: float):
        for item in enumerate(controller_sprites):
            index = item[0]
            data = item[1]
            data.sprite.visible = Controller.values[index]

    game.add_update_func(update_buttons)

    hero_data = SpriteData(game.width // 2, game.height // 2, "hero_front.png", vx=0, vy=0)
    create_sprites(game, [hero_data], include_graphics=include_graphics)
    controller = Controller()
    hero_data.sprite.apply_trait(MoveWithController(controller, 60, 60))
    hero_data.sprite.apply_trait(StayInBounds(8, 8, game.width - 8, game.height - 8))


def create_orbiting_planets_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created (12 sprites):
        - Two Earth sprites orbiting the centre of the screen (earth_1, earth_2)
        - Two Moon sprites orbiting their respective Earth sprites
        - Eight sprites following their respective Earth and Moon sprites (2 each)
    """
    earth_1 = Sprite(0, 0, AngularMotion(game.width // 2, game.height // 2, 25, math.pi / 4))
    if include_graphics:
        earth_1.apply_trait(DrawImage("earth.png"))

    earth_2 = Sprite(
        0, 0,
        AngularMotion(game.width // 2, game.height // 2, 25, math.pi / 4, start_angle=math.pi))
    if include_graphics:
        earth_2.apply_trait(DrawImage("earth.png"))

    earth_1_moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 15, math.pi))
    if include_graphics:
        earth_1_moon.apply_trait(DrawImage("moon.png"))

    earth_2_moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 15, math.pi))
    if include_graphics:
        earth_2_moon.apply_trait(DrawImage("moon.png"))

    game.add_child(earth_1)
    game.add_child(earth_2)
    earth_1.add_child(earth_1_moon)
    earth_2.add_child(earth_2_moon)

    follow_sprites: list[SpriteData] = [
        SpriteData(game.width // 2, game.height // 2, "7x3.png"),
        SpriteData(game.width // 2, game.height // 2, "john.png"),
        SpriteData(game.width // 2, game.height // 2, "8x8.png"),
        SpriteData(game.width // 2, game.height // 2, "7x7.png"),
        SpriteData(game.width // 2, game.height // 2, "7x3.png"),
        SpriteData(game.width // 2, game.height // 2, "8x8.png"),
        SpriteData(game.width // 2, game.height // 2, "hero_front.png"),
        SpriteData(game.width // 2, game.height // 2, "7x7.png"),
    ]

    create_sprites(game, follow_sprites, include_graphics=include_graphics, add_to_root=False)

    for item in enumerate([earth_1, earth_1, earth_1_moon, earth_1_moon, earth_2, earth_2, earth_2_moon, earth_2_moon]):
        index = item[0]
        parent = item[1]
        vx = 30 if index % 2 == 0 else 10
        vy = 10 if index % 2 == 0 else 30
        follow_sprites[index].sprite.apply_trait(FollowSprite(parent, vx, vy))
        parent.add_child(follow_sprites[index].sprite)


def create_oscillating_letters_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created (8 sprites):
        - 2 sprites oscillating/bouncing horizontally at the top of the screen
        - 2 sprites oscillating/bouncing horizontally at the bottom of the screen
        - 2 sprites oscillating/bouncing vertically at the left of the screen
        - 2 sprites oscillating/bouncing vertically at the right of the screen
    """
    # Add in the horizontally and vertically oscillating sprites.
    move_sprites: list[SpriteData] = [
        SpriteData(5, 5, "x.png", vx=30, vy=0, ax=30, ay=0),
        SpriteData(game.width - 5, 5, "y.png", vx=30, vy=0),
        SpriteData(game.width - 5, game.height - 5, "a.png", vx=-30, vy=0, ax=30, ay=0),
        SpriteData(5, game.height - 5, "b.png", vx=-30, vy=0),
        SpriteData(5, 5, "l.png", vx=0, vy=30, ax=0, ay=30),
        SpriteData(game.width - 5, 5, "r.png", vx=0, vy=30),
        SpriteData(game.width - 5, game.height - 5, "u.png", vx=0, vy=-30, ax=0, ay=30),
        SpriteData(5, game.height - 5, "d.png", vx=0, vy=-30),
    ]

    create_sprites(game, move_sprites, include_graphics=include_graphics)
    horizontal_oscillator = HorizontalOscillator(20, game.width - 20)
    vertical_oscillator = VerticalOscillator(20, game.height - 20)
    horizontal_bounce = HorizontalBounce(5, game.width - 5)
    vertical_bounce = VerticalBounce(5, game.height - 5)
    bound_velocity = BoundVelocity(-30, 30, -30, 30)

    for item in enumerate(move_sprites):
        index = item[0]
        data = item[1]
        if index % 2 == 0:
            data.sprite.apply_trait(horizontal_oscillator)
            data.sprite.apply_trait(vertical_oscillator)
        else:
            data.sprite.apply_trait(horizontal_bounce)
            data.sprite.apply_trait(vertical_bounce)

        data.sprite.apply_trait(bound_velocity)


def create_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created (33 sprites):
        - 12 sprites showing the status of each controller button
        - 1 hero sprite that can be moved around with the controller
        - Two Earth sprites orbiting the centre of the screen (earth_1, earth_2)
        - Two Moon sprites orbiting their respective Earth sprites
        - Eight sprites following their respective Earth and Moon sprites (2 each)
        - 2 sprites oscillating/bouncing horizontally at the top of the screen
        - 2 sprites oscillating/bouncing horizontally at the bottom of the screen
        - 2 sprites oscillating/bouncing vertically at the left of the screen
        - 2 sprites oscillating/bouncing vertically at the right of the screen
    """
    game.background_colour = (250, 120, 0)  # Orange
    create_controller_test_data(game, include_graphics)
    create_orbiting_planets_test_data(game, include_graphics)
    create_oscillating_letters_test_data(game, include_graphics)
