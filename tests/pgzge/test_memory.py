from pympler import asizeof

from pgzge.core import GameObject


class TestGameObjectSize:
    """
    The purpose of this test class is to evaluate the size of a GameObject instance.
    Whilst we expect most applications of GameObject will be for games written using
    Pygame Zero on a full-computer environment, there may be a desire to port this
    over to work in a more constrained environment such as CircuitPython.
    """

    def test_empty_object(self):
        obj = GameObject()
        print(f'Empty object: {asizeof.asizeof(obj)}')

    def test_with_name(self):
        obj = GameObject(name="root-object")
        print(f'Object with name: {asizeof.asizeof(obj)}')

    def test_with_two_children(self):
        obj = GameObject(children=[GameObject(), GameObject()])
        print(f'Object with two children: {asizeof.asizeof(obj)}')

    def test_with_four_children(self):
        obj = GameObject(
            children=[GameObject(), GameObject(), GameObject(), GameObject()])
        print(f'Object with four children: {asizeof.asizeof(obj)}')
