from pympler import asizeof

from core import GameObject


class TestGameObjectSize:
    """
    The purpose of this test class is to evaluate the size of a GameObject instance.
    The aim is to understand how much memory is used by a GameObject instance.
    Whilst we expect most applications of GameObject will be in games written in
    Desktop environments, there is no real reason why the engine could not be adapted
    to run in more constrained environments such as CircuitPython (assuming we break
    the dependencies on Pygame)..
    """

    def test_empty_object(self):
        obj = GameObject()
        print(f'Empty object: {asizeof.asizeof(obj)}')

    def test_with_name(self):
        obj = GameObject("root-object")
        print(f'Object with name: {asizeof.asizeof(obj)}')

    def test_with_two_children(self):
        obj = GameObject(children=[GameObject(), GameObject()])
        print(f'Object with two children: {asizeof.asizeof(obj)}')

    def test_with_four_children(self):
        obj = GameObject(children=[GameObject(), GameObject(), GameObject(), GameObject()])
        print(f'Object with four children: {asizeof.asizeof(obj)}')
