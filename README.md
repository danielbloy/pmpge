# Python Multi-Platform Game Engine (pmpge)

An easy-to-use Game Engine that works with Pygame Zero on desktop computers and also with
CircuitPython and MicroPython devices. It is designed for use in Coding Clubs.

Please see my website [Code Club Adventures](http://codeclubadventures.com/) for more coding materials.

## Overview

This project originated from a desire to make it as simple as possible for students at my
coding club to make their own games in Python using Pygame Zero. There were two primary
drivers:

1. Remove the need to write the same common code in each game.
2. Avoid the need to modify code from earlier steps, focussing on incremental addition
   rather than modification

So why these aims? Removing the need to write the same common code in each game is boring
for the students and takes up time that is better spent being creative writing new code.
The aim is to allow the students to focus on the game and not the "engine".

Python is a great language for beginnings to start with but even so, writing Python code
can be hard for all newcomers. It is easy to get your indentation wrong or mix parentheses
with brackets. It's even harder to go back and change code you've already written, particularly
if you have modified or extended that code from the original. When students break and then cant
fix their previously working program it leads to frustration and loss of confidence.

It is also difficult to write clear and concise instructions explaining how to modify existing
code. It can very quickly get verbose and hard to follow. I therefore try to avoid this where
possible and focus on incremental addition of new code rather than modification of existing code.

The origins of this project are from the Python Pygame Zero games that I have written for my
coding club. Head over
to [Code Club adventures - games with Pygame Zero](https://codeclubadventures.co.uk/advancing/#games-with-pygame-zero)
to take a look.

A stretch goal for this project is to abstract the underlying host framework (Pygame Zero) so
that support can be added relatively easily for other environments at a later date. The other
environments are primarily CircuitPython which already provides a great abstraction layer. The
driver for this is that writing games for devices is tricky in a Code Club other that using the
MakeCode platform as the code/test cycle is tiresome and tricky for young people. This framework
aims to make development easy on a desktop which can then be easily copied across to the device.
The main limitation is RAM but with the new Pico 2350 and ESP32 S3 boards offering 2Mb or more
of RAM, it is not the limtation is once was.

## Project structure

The structure of the `pmpge`project is arranged in the following files (listed in order of
importance):

* `controller.py`  - Provides a standard controller abstraction offering different "levels" of
  controller so games can adapt to what the environment offers.
* `environment.py` - Provides information about the environment the engine is operating in such
  as whether it is running on a desktop or microcontroller and which type of Python.
* `game.py`        - Provides the `Game` class which is a helper class used to run the game.
* `game_object.py` - Provides the `GameObject` class which is the basis of `pmpge`.
* `graphics.py`    - Provides a standard graphics abstraction to support different environments.
* `palette.py`     - Provides the `Palette` class for managing colour palettes.
* `sound.py`       - Provides a standard sound abstraction to support different environments.
* `sprite.py`      - Provides the `Sprite` class which is used to represent a GameObject with
  position.
* `system.py`      - Provides a standard system abstraction to support different host systems.
* `traits`         - Directory containing a range of traits that can be added to a `GameObject`.

Some sample games written using the `pmpge` framework can be found in `games` and examples
demonstrating how to use the framework can be found in `examples`.

## Setting up a Development Environment

The project has been developed using the [PyCharm IDE](https://www.jetbrains.com/pycharm/)
with a VENV for Python (using Python 3.12) with tests written using `pytest` (see
[pytest](https://docs.pytest.org/en/8.2.x/) for more information).

In PyCharm, the following "Project Structure" is used:

![Project Structure](./project_structure.png)

## Reference hardware

TODO: Use EdgeBadge/PyBadge for CircuitPython.
TODO: Use vanilla Pico 2 with 160x128 display for micropython and circuit python
TODO: Could also specify Tufty for MicroPython

## License

All materials provided in this project is licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0
International License. To view a copy of this license, visit
<https://creativecommons.org/licenses/by-nc-sa/4.0/>.

In summary, this means that you are free to:

* **Share** — copy and redistribute the material in any medium or format.
* **Adapt** — remix, transform, and build upon the material.

Provided you follow these terms:

* **Attribution** — You must give appropriate credit , provide a link to the license, and indicate
  if changes were made.
  You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you
  or your use.
* **NonCommercial** — You may not use the material for commercial purposes.
* **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your
  contributions under the
  same license as the original.