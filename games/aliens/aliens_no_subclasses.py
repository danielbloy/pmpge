# This version of aliens has been modified to demonstrate additional techniques,
# particularly how to create different types of Sprite without using subclasses.
# Original source material: https://codeclubadventures.co.uk/python/pygame/aliens/
import os
from typing import Any

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import pgzrun
from pgzge.core import Game, GameObject
from pgzero.clock import Clock
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen
from random import randint
import time

clock: Clock
screen: Screen
keyboard: Keyboard
pgzge: Game = Game()

WIDTH = 600
HEIGHT = 700

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

STARS_MIN_SPEED = 75
STARS_MAX_SPEED = 150
STARS_TOTAL = 200


def create_starfield(n) -> GameObject:
    def activate(obj):
        obj.n = n
        obj.stars = [
            (
                randint(0, WIDTH),  # x position
                randint(0, HEIGHT),  # y position
                randint(STARS_MIN_SPEED, STARS_MAX_SPEED)  # speed
            )
            for _ in range(obj.n)
        ]

    def draw(obj, surface: Any):
        for star in obj.stars:
            screen.draw.filled_circle((star[0], star[1]), 1, WHITE)

    def update(obj, dt: float):
        # STEP A: Move stars down the screen
        obj.stars = [
            (
                star[0],  # x position
                star[1] + (star[2] * dt),  # y position
                star[2]  # speed
            )
            for star in obj.stars
        ]

        # STEP B: Remove stars that have moved off the bottom of the screen
        obj.stars = [
            (
                star[0],
                star[1],
                star[2]
            )
            for star in obj.stars
            if star[1] < HEIGHT
        ]

        # STEP C: Add new stars at the top to maintain the total number of stars
        for _ in range(obj.n - len(obj.stars)):
            obj.stars.append(
                (
                    randint(0, WIDTH),  # x position
                    0,  # y position - top of screen
                    randint(STARS_MIN_SPEED, STARS_MAX_SPEED)  # speed
                )
            )

    game_object = GameObject(
        activate_handler=activate,
        draw_handler=draw,
        update_handler=update)
    pgzge.add_child(game_object)
    return game_object


starfield = create_starfield(STARS_TOTAL)

# Step 3: Adding the title screen
high_score = 20000
score = 0
lives = 3
stage = 1


def create_title_screen() -> GameObject:
    def activate(obj):
        obj.draw_press_space = True
        obj.press_space_transition = time.time() + 0.5

    def draw(obj, surface):
        screen.draw.text("HIGH SCORE",  # NOTE: Code modified to use screen directly.
                         midtop=(WIDTH / 2, 0),
                         color=RED,
                         fontsize=36)
        screen.draw.text(f"{high_score}",  # NOTE: Code modified to use screen directly.
                         midtop=(WIDTH / 2, 30),
                         color=WHITE,
                         fontsize=36)

        if obj.draw_press_space:
            screen.draw.text("PRESS SPACE TO START",  # NOTE: Code modified to use screen directly.
                             midtop=(WIDTH / 2, 250),
                             color=CYAN,
                             fontsize=36)

        screen.blit('player', (75, 395))
        screen.blit('player', (75, 470))
        screen.blit('player', (75, 545))

        screen.draw.text("1ST BONUS FOR 30000 PTS",  # NOTE: Code modified to use screen directly.
                         midtop=(WIDTH / 2, 400),
                         color=YELLOW,
                         fontsize=36)

        screen.draw.text("2ND BONUS FOR 120000 PTS",  # NOTE: Code modified to use screen directly.
                         midtop=(WIDTH / 2, 475),
                         color=YELLOW,
                         fontsize=36)

        screen.draw.text("AND FOR EVERY 120000 PTS",  # NOTE: Code modified to use screen directly.
                         midtop=(WIDTH / 2, 550),
                         color=YELLOW,
                         fontsize=36)

        screen.draw.text("INSPIRED BY GALAGA FROM NAMCO LTD.",  # NOTE: Code modified to use screen directly.
                         midtop=(WIDTH / 2, 650),
                         color=WHITE,
                         fontsize=36)

    def update(obj, dt):
        now = time.time()
        if obj.press_space_transition < now:
            obj.press_space_transition = now + 0.5
            obj.draw_press_space = not obj.draw_press_space

    game_object = GameObject(
        activate_handler=activate,
        draw_handler=draw,
        update_handler=update)
    pgzge.add_child(game_object)
    return game_object


title_screen = create_title_screen()


def draw():
    pgzge.draw(screen.surface)


def update(dt):
    pgzge.update(dt)


pgzrun.go()