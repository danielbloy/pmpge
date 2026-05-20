from pmpge.controller import Controller


def test_static_properties_lengths():
    """
    Test the static properties of the Controller class for initial lengths.
    """
    current = Controller.values
    previous = Controller._previous
    changed = Controller.changed
    assert len(current) == 12
    assert len(previous) == 12
    assert len(changed) == 12


def test_reset():
    """
    Validates that reset() works correctly.
    """
    Controller.reset()
    current = Controller.values
    previous = Controller._previous
    changed = Controller.changed
    for i in range(len(current)):
        assert current[i] == False
        assert previous[i] == False
        assert changed[i] == False

    # Now set everything to True
    for i in range(len(current)):
        current[i] = True
        previous[i] = True
        changed[i] = True

    # Now reset and validate.
    Controller.reset()
    for i in range(len(current)):
        assert current[i] == False
        assert previous[i] == False
        assert changed[i] == False


def test_buttons():
    """
    Validates that the buttons register correctly. This is a long but trivial test.
    """
    Controller.reset()

    controller = Controller()
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_START] = True
    assert controller.start == True
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_SELECT] = True
    assert controller.start == False
    assert controller.select == True
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_LEFT] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == True
    assert controller.l == True
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_RIGHT] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == True
    assert controller.r == True
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_UP] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == True
    assert controller.u == True
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_DOWN] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == True
    assert controller.d == True
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_A] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == True
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_B] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == True
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_X] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == True
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_Y] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == True
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_LS] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == True
    assert controller.ls == True
    assert controller.right_shoulder == False
    assert controller.rs == False

    Controller.reset()
    Controller.values[Controller.BUTTON_RS] = True
    assert controller.start == False
    assert controller.select == False
    assert controller.left == False
    assert controller.l == False
    assert controller.right == False
    assert controller.r == False
    assert controller.up == False
    assert controller.u == False
    assert controller.down == False
    assert controller.d == False
    assert controller.a == False
    assert controller.b == False
    assert controller.x == False
    assert controller.y == False
    assert controller.left_shoulder == False
    assert controller.ls == False
    assert controller.right_shoulder == True
    assert controller.rs == True
# TODO: Add tests for the changed and current values.
# TODO: Test events
