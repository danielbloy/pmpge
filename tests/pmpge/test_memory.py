"""
The purpose of these tests is to evaluate the size of a GameObject instance.
Whilst we expect most applications of GameObject will be for games written using
Pygame Zero on a full-computer environment, there may be a desire to port this
over to work in a more constrained environment such as CircuitPython.
"""
from pympler import asizeof

from pmpge.game_object import GameObject


def test_empty_object():
    obj = GameObject()
    print(f'Empty object: {asizeof.asizeof(obj)}')


def test_with_name():
    obj = GameObject(name="root-object")
    print(f'Object with name: {asizeof.asizeof(obj)}')


def test_with_two_children():
    obj = GameObject(children=[GameObject(), GameObject()])
    print(f'Object with two children: {asizeof.asizeof(obj)}')


def test_with_four_children():
    obj = GameObject(
        children=[GameObject(), GameObject(), GameObject(), GameObject()])
    print(f'Object with four children: {asizeof.asizeof(obj)}')
