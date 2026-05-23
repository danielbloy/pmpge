from pmpge.controller import Controller
from pmpge.game_object import GameObject
from traits.controller import OnPressed


def test_constructor():
    """
    Some simple tests to validate the constructor works. There will be
    no events fired during this test.
    """
    controller = Controller()
    count = 0

    def increment(go: GameObject):
        nonlocal count
        count += 1

    # Test with no events
    trait = OnPressed(controller)
    assert count == 0
    assert trait.controller == controller
    assert trait.on_pressed == ()

    # Test with one event
    trait = OnPressed(controller, (Controller.BUTTON_A, increment))
    trait.update(0)
    assert count == 0
    assert trait.controller == controller
    assert len(trait.on_pressed) == 1

    # Test with two events
    trait = OnPressed(controller, (Controller.BUTTON_A, increment), (Controller.BUTTON_B, increment))
    trait.update(0)
    assert count == 0
    assert trait.controller == controller
    assert len(trait.on_pressed) == 2

    # Test with 4 events
    trait = OnPressed(controller,
                      (Controller.BUTTON_A, increment),
                      (Controller.BUTTON_B, increment),
                      (Controller.BUTTON_X, increment),
                      (Controller.BUTTON_Y, increment))
    trait.update(0)
    assert count == 0
    assert trait.controller == controller
    assert len(trait.on_pressed) == 4


def test_single_event_received():
    """
    Validates that a single OnPressed event is received but only if
    we have an event for it.
    """
    values = [False for _ in range(12)]
    Controller.reset()

    controller = Controller()
    count = 0
    go = None

    def increment(g: GameObject):
        nonlocal go, count
        count += 1
        go = g

    trait = OnPressed(controller, (Controller.BUTTON_A, increment))
    trait.update(0)
    assert count == 0
    assert trait.controller == controller
    assert len(trait.on_pressed) == 1

    # Press a button we don't have an event for.
    values[Controller.BUTTON_RS] = True
    Controller.update(values)
    trait.update(0)
    assert count == 0
    assert go is None

    # Press a button we do have an event for.
    values[Controller.BUTTON_A] = True
    Controller.update(values)
    trait.update(0)
    assert count == 1
    assert go == trait
    go = None

    # Press another button we don't have an event for.
    values[Controller.BUTTON_START] = True
    Controller.update(values)
    trait.update(0)
    assert count == 1
    assert go is None

    # Release the button we are interested in, no event
    values[Controller.BUTTON_A] = False
    Controller.update(values)
    trait.update(0)
    assert count == 1
    assert go is None

    # Press a button we do have an event for.
    values[Controller.BUTTON_A] = True
    Controller.update(values)
    trait.update(0)
    assert count == 2
    assert go == trait


def test_multiple_event_received():
    """
    Validates that we can receive multiple OnPressed events but only if
    we have events for them.
    """
    values = [False for _ in range(12)]
    Controller.reset()

    controller = Controller()
    count_a = 0
    count_b = 0
    go_a = None
    go_b = None

    def button_a(g: GameObject):
        nonlocal go_a, count_a
        count_a += 1
        go_a = g

    def button_b(g: GameObject):
        nonlocal go_b, count_b
        count_b += 1
        go_b = g

    trait = OnPressed(controller, (Controller.BUTTON_A, button_a), (Controller.BUTTON_B, button_b))
    trait.update(0)
    assert count_a == 0
    assert count_b == 0

    # Press a button we don't have an event for.
    values[Controller.BUTTON_RS] = True
    Controller.update(values)
    trait.update(0)
    assert count_a == 0
    assert go_a is None
    assert count_b == 0
    assert go_b is None

    # Press a button we do have an event for.
    values[Controller.BUTTON_A] = True
    Controller.update(values)
    trait.update(0)
    assert count_a == 1
    assert go_a == trait
    assert count_b == 0
    assert go_b is None

    go_a = None

    # Release the button we are interested in, no event
    values[Controller.BUTTON_A] = False
    Controller.update(values)
    trait.update(0)
    assert count_a == 1
    assert go_a is None
    assert count_b == 0
    assert go_b is None

    # Press both buttons we have events for
    values[Controller.BUTTON_A] = True
    values[Controller.BUTTON_B] = True
    values[Controller.BUTTON_LS] = True
    Controller.update(values)
    trait.update(0)
    assert count_a == 2
    assert go_a == trait
    assert count_b == 1
    assert go_b == trait


def test_same_button_multiple_handlers():
    """
    Validates that we can receive multiple OnPressed events but only if
    we have events for them.
    """
    values = [False for _ in range(12)]
    Controller.reset()

    controller = Controller()
    count_1 = 0
    count_2 = 0

    def button_1(g: GameObject):
        nonlocal count_1
        count_1 += 1

    def button_2(g: GameObject):
        nonlocal count_2
        count_2 += 1

    trait = OnPressed(controller, (Controller.BUTTON_A, button_1), (Controller.BUTTON_A, button_2))
    trait.update(0)
    assert count_1 == 0
    assert count_2 == 0

    # Press a button we don't have an event for.
    values[Controller.BUTTON_RS] = True
    Controller.update(values)
    trait.update(0)
    assert count_1 == 0
    assert count_2 == 0

    # Press a button we do have an event for, it should trigger both.
    values[Controller.BUTTON_A] = True
    Controller.update(values)
    trait.update(0)
    assert count_1 == 1
    assert count_2 == 1
