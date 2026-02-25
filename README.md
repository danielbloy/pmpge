# Pygame Zero Game Engine (pgzge)

An easy-to-use Game Engine that works with Pygame Zero and designed for use in Coding Clubs.

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

it is also difficult to write clear and concise instructions explaining how to modify existing
code. It can very quickly get verbose and hard to follow. I therefore try to avoid this where
possible and focus on incremental addition of new code rather than modification of existing code.

The origins of this project are from the Python Pygame Zero games that I have written for my coding
club. Head over
to [Code Club adventures - games with Pygame Zero](https://codeclubadventures.co.uk/advancing/#games-with-pygame-zero)
to take a look.

## Project structure

The structure of the `pgzge`project is arranged in the following files (listed in
order of importance):

* core - required for every `pgzge` project as it provides the `Game` and `GameObject` classes.

Some sample games written using the `pgzge` framework can be found in `games` and examples
demonstrating how to use the framework can be found in `examples`.

## Setting up a Development Environment

The project has been developed using the [PyCharm IDE](https://www.jetbrains.com/pycharm/)
with a VENV for Python (using Python 3.12) with tests written using `pytest` (see
[pytest](https://docs.pytest.org/en/8.2.x/) for more information).

In PyCharm, the following "Project Structure" is used:

![Project Structure](./project_structure.png)

## License

All materials provided in this project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International License. To view a copy of this license, visit
<https://creativecommons.org/licenses/by-nc-sa/4.0/>.

In summary, this means that you are free to:

* **Share** — copy and redistribute the material in any medium or format.
* **Adapt** — remix, transform, and build upon the material.

Provided you follow these terms:

* **Attribution** — You must give appropriate credit , provide a link to the license, and indicate if changes were made.
  You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* **NonCommercial** — You may not use the material for commercial purposes.
* **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the
  same license as the original.
* 