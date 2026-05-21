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


def test_update_pressed_and_released():
    """
    Validates pressed and released works. Only tests a subset of buttons.
    """
    values = [False for _ in range(12)]
    expected_previous = [False for _ in range(12)]
    expected_changed = [False for _ in range(12)]

    current = Controller.values
    previous = Controller._previous
    changed = Controller.changed
    Controller.reset()

    # Set everything to false should result in no changes.
    Controller.update(values)
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed

    # Now try the first button.
    values[0] = True
    expected_changed[0] = True
    Controller.update(values)
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed

    # Now the second button, the first stays on but is no longer flagged as pressed.
    values[1] = True
    expected_changed[0] = False
    expected_changed[1] = True
    expected_previous[0] = True
    Controller.update(values)
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed

    # Now release the first button, this will mark it changed.
    values[0] = False
    expected_changed[0] = True
    expected_changed[1] = False
    expected_previous[1] = True
    Controller.update(values)
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed

    # Now change several buttons at once.
    Controller.reset()
    values = [False for _ in range(12)]
    expected_previous = [False for _ in range(12)]
    expected_changed = [False for _ in range(12)]
    values[3], values[7], values[8], values[11] = True, True, True, True
    expected_changed[3], expected_changed[7], expected_changed[8], expected_changed[11] = True, True, True, True
    expected_previous[3], expected_previous[7], expected_previous[8], expected_previous[11] = False, False, False, False
    Controller.update(values)
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed

    # Run again which should reset the changed flags and previous values
    Controller.update(values)
    expected_changed[3], expected_changed[7], expected_changed[8], expected_changed[11] = False, False, False, False
    expected_previous[3], expected_previous[7], expected_previous[8], expected_previous[11] = True, True, True, True
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed

    # Now release all buttons.
    values[3], values[7], values[8], values[11] = False, False, False, False
    Controller.update(values)
    expected_changed[3], expected_changed[7], expected_changed[8], expected_changed[11] = True, True, True, True
    expected_previous[3], expected_previous[7], expected_previous[8], expected_previous[11] = True, True, True, True
    assert current == values
    assert previous == expected_previous
    assert changed == expected_changed


def test_validate_all_buttons():
    """
    Validates that update works with each of the buttons. This ensures that
    the controller state is correctly updated based on button presses.
    """

    current = Controller.values
    previous = Controller._previous
    changed = Controller.changed

    for i in range(len(current)):
        Controller.reset()
        values = [False for _ in range(12)]
        expected_previous = [False for _ in range(12)]
        expected_changed = [False for _ in range(12)]

        # Enable the button
        values[i] = True
        expected_changed[i] = True
        Controller.update(values)
        assert current == values
        assert previous == expected_previous
        assert changed == expected_changed

        # Update again which set the previous value and resets changed
        expected_changed[i] = False
        expected_previous[i] = True
        Controller.update(values)
        assert current == values
        assert previous == expected_previous
        assert changed == expected_changed

        # Disable the button which triggers another change
        values[i] = False
        expected_changed[i] = True
        Controller.update(values)
        assert current == values
        assert previous == expected_previous
        assert changed == expected_changed

        # Update again which set the previous value and resets changed
        expected_changed[i] = False
        expected_previous[i] = False
        Controller.update(values)
        assert current == values
        assert previous == expected_previous
        assert changed == expected_changed


def test_button_events():
    """
    Validates that events() correctly returns the events that have occurred since
    the last update(). This wil lonly return the events that have fired.
    """
    values = [False for _ in range(12)]

    # No events
    Controller.reset()
    events = Controller.events()
    assert events == []

    # Still no events
    Controller.update(values)
    events = Controller.events()
    assert events == []

    # Single event by pressing Y button
    values[Controller.BUTTON_Y] = True
    Controller.update(values)
    events = Controller.events()
    assert events == [(Controller.BUTTON_Y, True)]

    # The next update will result in no events
    Controller.update(values)
    events = Controller.events()
    assert events == []

    # Release Y button
    values[Controller.BUTTON_Y] = False
    Controller.update(values)
    events = Controller.events()
    assert events == [(Controller.BUTTON_Y, False)]

    # Now try a series of button presses and releases.
    values[Controller.BUTTON_UP] = True
    values[Controller.BUTTON_X] = True
    values[Controller.BUTTON_RS] = True
    Controller.update(values)
    events = Controller.events()
    assert events == [(Controller.BUTTON_UP, True), (Controller.BUTTON_X, True), (Controller.BUTTON_RS, True)]

    Controller.update(values)
    events = Controller.events()
    assert events == []

    # Release one button and press another
    values[Controller.BUTTON_UP] = False
    values[Controller.BUTTON_DOWN] = True
    Controller.update(values)
    events = Controller.events()
    assert events == [(Controller.BUTTON_UP, False), (Controller.BUTTON_DOWN, True)]

    # Release all buttons
    values = [False for _ in range(12)]
    Controller.update(values)
    events = Controller.events()
    assert events == [(Controller.BUTTON_DOWN, False), (Controller.BUTTON_X, False), (Controller.BUTTON_RS, False)]


def test_is_and_has_methods():
    """
    Validates that the is_ and has_ methods work correctly. These methods are convenience
    methods around accessing the Controller.values and Controller.changed arrays directly.
    """
    values = [False for _ in range(12)]

    # No events, nothing pressed
    Controller.reset()
    assert Controller.is_pressed(Controller.BUTTON_UP) == False
    assert Controller.is_released(Controller.BUTTON_UP) == True
    assert Controller.has_changed(Controller.BUTTON_UP) == False
    assert Controller.has_pressed(Controller.BUTTON_UP) == False
    assert Controller.has_released(Controller.BUTTON_UP) == False

    assert Controller.is_pressed(Controller.BUTTON_A) == False
    assert Controller.is_released(Controller.BUTTON_A) == True
    assert Controller.has_changed(Controller.BUTTON_A) == False
    assert Controller.has_pressed(Controller.BUTTON_A) == False
    assert Controller.has_released(Controller.BUTTON_A) == False

    assert Controller.is_pressed(Controller.BUTTON_RS) == False
    assert Controller.is_released(Controller.BUTTON_RS) == True
    assert Controller.has_changed(Controller.BUTTON_RS) == False
    assert Controller.has_pressed(Controller.BUTTON_RS) == False
    assert Controller.has_released(Controller.BUTTON_RS) == False

    # Press a single button
    values[Controller.BUTTON_RS] = True
    Controller.update(values)
    assert Controller.is_pressed(Controller.BUTTON_RS) == True
    assert Controller.is_released(Controller.BUTTON_RS) == False
    assert Controller.has_changed(Controller.BUTTON_RS) == True
    assert Controller.has_pressed(Controller.BUTTON_RS) == True
    assert Controller.has_released(Controller.BUTTON_RS) == False

    # Update clears the changed flags
    Controller.update(values)
    assert Controller.is_pressed(Controller.BUTTON_RS) == True
    assert Controller.is_released(Controller.BUTTON_RS) == False
    assert Controller.has_changed(Controller.BUTTON_RS) == False
    assert Controller.has_pressed(Controller.BUTTON_RS) == False
    assert Controller.has_released(Controller.BUTTON_RS) == False

    # Now release the button
    values[Controller.BUTTON_RS] = False
    Controller.update(values)
    assert Controller.is_pressed(Controller.BUTTON_RS) == False
    assert Controller.is_released(Controller.BUTTON_RS) == True
    assert Controller.has_changed(Controller.BUTTON_RS) == True
    assert Controller.has_pressed(Controller.BUTTON_RS) == False
    assert Controller.has_released(Controller.BUTTON_RS) == True

    # Update clears the changed flags
    Controller.update(values)
    assert Controller.is_pressed(Controller.BUTTON_RS) == False
    assert Controller.is_released(Controller.BUTTON_RS) == True
    assert Controller.has_changed(Controller.BUTTON_RS) == False
    assert Controller.has_pressed(Controller.BUTTON_RS) == False
    assert Controller.has_released(Controller.BUTTON_RS) == False

    # Now we try with two
    values[Controller.BUTTON_UP] = True
    values[Controller.BUTTON_A] = True
    Controller.update(values)

    assert Controller.is_pressed(Controller.BUTTON_UP) == True
    assert Controller.is_released(Controller.BUTTON_UP) == False
    assert Controller.has_changed(Controller.BUTTON_UP) == True
    assert Controller.has_pressed(Controller.BUTTON_UP) == True
    assert Controller.has_released(Controller.BUTTON_UP) == False

    assert Controller.is_pressed(Controller.BUTTON_A) == True
    assert Controller.is_released(Controller.BUTTON_A) == False
    assert Controller.has_changed(Controller.BUTTON_A) == True
    assert Controller.has_pressed(Controller.BUTTON_A) == True
    assert Controller.has_released(Controller.BUTTON_A) == False
