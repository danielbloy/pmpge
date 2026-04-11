import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'150,100'

from pgzero.clock import Clock
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen

from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.palette import CYAN, RED, WHITE, YELLOW
from pmpge.sprite import Sprite
from pmpge.traits.controller import MoveWithController
from pmpge.traits.graphics import DrawImage, DrawText
from pmpge.traits.physics import Velocity
from pmpge.traits.position import StayInBounds, RelativeToParent, Position

clock: Clock
keyboard: Keyboard
screen: Screen

game: Game = Game(600, 700)

# Step 2: Adding the starfield
STARS_MIN_SPEED = 75
STARS_MAX_SPEED = 150
STARS_TOTAL = 200

from random import randint


class StarField(GameObject):

    def __init__(self, n):
        super().__init__()
        self.n = n
        self.stars = [
            (
                randint(0, game.width),  # x position
                randint(0, game.height),  # y position
                randint(STARS_MIN_SPEED, STARS_MAX_SPEED)  # speed
            )
            for _ in range(n)
        ]

    def draw(self, surface):
        for star in self.stars:
            screen.draw.filled_circle((star[0], star[1]), 1,
                                      WHITE)  # NOTE: Code modified to use screen directly.

    def update(self, dt):
        # STEP A: Move stars down the screen
        self.stars = [
            (
                star[0],  # x position
                star[1] + (star[2] * dt),  # y position
                star[2]  # speed
            )
            for star in self.stars
        ]

        # STEP B: Remove stars that have moved off the bottom of the screen
        self.stars = [
            (
                star[0],
                star[1],
                star[2]
            )
            for star in self.stars
            if star[1] < game.height
        ]

        # STEP C: Add new stars at the top to maintain the total number of stars
        for _ in range(self.n - len(self.stars)):
            self.stars.append(
                (
                    randint(0, game.width),  # x position
                    0,  # y position - top of screen
                    randint(STARS_MIN_SPEED, STARS_MAX_SPEED)  # speed
                )
            )


starfield = StarField(STARS_TOTAL)
game.add_child(starfield)  # NOTE: Additional code

# Step 3: Adding the title screen
high_score = 20000
score = 0
lives = 3
stage = 1

import time


class TitleScreen(GameObject):
    def __init__(self):
        super().__init__()
        self.draw_press_space = True
        self.press_space_transition = 0

    def activated(self):
        self.draw_press_space = True
        self.press_space_transition = time.time() + 0.5

    def draw(self, surface):
        screen.draw.text("HIGH SCORE",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 0),
                         color=RED,
                         fontsize=36)
        screen.draw.text(f"{high_score}",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 30),
                         color=WHITE,
                         fontsize=36)

        if self.draw_press_space:
            screen.draw.text("PRESS SPACE TO START",  # NOTE: Code modified to use screen directly.
                             midtop=(game.width / 2, 250),
                             color=CYAN,
                             fontsize=36)

        screen.blit('player', (75, 395))
        screen.blit('player', (75, 470))
        screen.blit('player', (75, 545))

        screen.draw.text("1ST BONUS FOR 30000 PTS",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 400),
                         color=YELLOW,
                         fontsize=36)

        screen.draw.text("2ND BONUS FOR 120000 PTS",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 475),
                         color=YELLOW,
                         fontsize=36)

        screen.draw.text("AND FOR EVERY 120000 PTS",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 550),
                         color=YELLOW,
                         fontsize=36)

        screen.draw.text("INSPIRED BY GALAGA FROM NAMCO LTD.",
                         # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 650),
                         color=WHITE,
                         fontsize=36)

    def update(self, dt):
        now = time.time()
        if self.press_space_transition < now:
            self.press_space_transition = now + 0.5
            self.draw_press_space = not self.draw_press_space


title_screen = TitleScreen()
game.add_child(title_screen)  # NOTE: Additional code

# Step 4: Add a game HUD
LOWER_BORDER_HEIGHT = 40
UPPER_BORDER_HEIGHT = 50
LOWER_BORDER_START = game.height - LOWER_BORDER_HEIGHT


class GameHud(GameObject):
    def __init__(self):
        super().__init__(active=False)  # NOTE: Code modified to explicitly set active to False.
        self.draw_one_up = True
        self.one_up_transition = 0
        self.show_stage = True
        self.show_stage_left = 0

    def activated(self):
        self.draw_one_up = True
        self.one_up_transition = time.time() + 0.5
        self.show_stage = True
        self.show_stage_left = 2.0

    def draw(self, draw):
        screen.draw.text("HIGH SCORE",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 0),
                         color=RED,
                         fontsize=36)
        screen.draw.text(f"{high_score}",  # NOTE: Code modified to use screen directly.
                         midtop=(game.width / 2, 30),
                         color=WHITE,
                         fontsize=36)

        if self.draw_one_up:
            screen.draw.text("1UP",  # NOTE: Code modified to use screen directly.
                             topleft=(20, 0),
                             color=RED,
                             fontsize=36)

        screen.draw.text(f"{score}",  # NOTE: Code modified to use screen directly.
                         topleft=(20, 30),
                         color=WHITE,
                         fontsize=36)

        if self.show_stage:
            screen.draw.text(f"STAGE {stage}",  # NOTE: Code modified to use screen directly.
                             midtop=(game.width / 2, 300),
                             color=CYAN,
                             fontsize=36)

        for i in range(lives):
            screen.blit('player', (5 + (37 * i), LOWER_BORDER_START + 4))

        for i in range(stage):
            screen.blit('stage_marker',
                        ((game.width - 5) - (16 * (i + 1)), LOWER_BORDER_START + 4))

    def update(self, dt):
        self.show_stage_left -= dt
        self.show_stage = self.show_stage_left > 0

        now = time.time()
        if self.one_up_transition < now:
            self.one_up_transition = now + 0.5
            self.draw_one_up = not self.draw_one_up


game_hud = GameHud()
game.add_child(game_hud)  # NOTE: Additional code


def new_game(dt):
    global score, lives, stage
    if title_screen.active and keyboard.space:
        score = 0
        lives = 3
        stage = 1

        title_screen.active = False
        game_hud.active = True


game.add_update_func(new_game)  # NOTE: modified from `update_funcs.append(new_game)`.

PLAYER_SHIP_HEIGHT = 32
PLAYER_SHIP_WIDTH = 32
PLAYER_SHIP_MAX_LEFT = (PLAYER_SHIP_WIDTH / 2)
PLAYER_SHIP_MAX_RIGHT = game.width - (PLAYER_SHIP_WIDTH / 2)
PLAYER_SHIP_START_HEIGHT = LOWER_BORDER_START - (PLAYER_SHIP_HEIGHT / 2)

player = Sprite(
    game.width / 2, PLAYER_SHIP_START_HEIGHT,
    DrawImage('player'))

controller = Controller()
player.apply_trait(MoveWithController(200, 0, controller))
player.apply_trait(StayInBounds(PLAYER_SHIP_MAX_LEFT, 0, PLAYER_SHIP_MAX_RIGHT, game.height))
game_hud.add_child(player)

player.add_child(
    Sprite(
        0, 0,
        RelativeToParent(16, 16),
        DrawText(lambda obj: f"{obj.pos}")
    )
).add_child(
    Sprite(
        0, 0,
        RelativeToParent(16, -16),
        DrawText(f"{lives}")
    )
)

sprite = GameObject(Position(game.width / 2, PLAYER_SHIP_START_HEIGHT),
                    DrawImage('alien_a_1'),
                    Velocity(15, -25))
sprite.add_child(
    Sprite(
        0, 0,
        RelativeToParent(16, 16),
        DrawText(lambda obj: f"{obj.pos}")
    )
)
game.add_child(sprite)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


game.run()
