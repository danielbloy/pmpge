import pytest

from pmpge.game import Game
from pmpge.game_object import GameObject
from tests.pmpge.test_utilities import with_config_file


def test_empty_constructor():
    """
    Validates that a Game object can be created with an empty constructor and work.
    """
    game = Game()
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (0, 0, 0)
    assert game.root
    assert len(game.children) == 0


def test_constructor_with_width_and_height():
    """
    Validates that both a width and height must be specified for a Game to be created.
    """
    with pytest.raises(ValueError):
        Game(width=100)

    with pytest.raises(ValueError):
        Game(height=100)

    game = Game(width=100, height=100)
    assert game.width == 100
    assert game.height == 100
    assert game.background_color == (0, 0, 0)
    assert game.root
    assert len(game.children) == 0


def test_constructor_with_config():
    """
    Validates that the configuration is used when width and height are not specified.
    """

    def validate():
        # Using the default configuration from the config file.
        game = Game()
        assert game.width == 800
        assert game.height == 300

        # Override the default configuration from the config file.
        game = Game(width=320, height=240)
        assert game.width == 320
        assert game.height == 240

        return True

    with_config_file(
        "SCREEN_WIDTH = 800\nSCREEN_HEIGHT = 300\n", validate)


def test_constructor_with_background_colour():
    """
    Validates that a Game can be created with a custom background colour.
    """
    game = Game()
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (0, 0, 0)
    assert game.root
    assert len(game.children) == 0

    game = Game(background_color=(1, 2, 3))
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (1, 2, 3)
    assert game.root
    assert len(game.children) == 0

    game = Game(background_color=(6, 5, 4))
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (6, 5, 4)
    assert game.root
    assert len(game.children) == 0


def test_adding_and_removing_children():
    """
    These are simple tests as Game just passes it on to the root object.
    """
    game = Game()
    assert game.root
    assert len(game.children) == 0

    frank = GameObject(name="Frank")
    bob = GameObject(name="Bob")

    game.add_child(frank)
    assert game.root
    assert len(game.children) == 1
    assert frank in game.children
    assert game.children[0].name == "Frank"

    game.add_child(bob)
    assert game.root
    assert len(game.children) == 2
    assert bob in game.children
    assert game.children[0].name == "Frank"
    assert game.children[1].name == "Bob"

    game.remove_child(frank)
    assert game.root
    assert len(game.children) == 1
    assert bob in game.children
    assert game.children[0].name == "Bob"

    game.remove_child(bob)
    assert game.root
    assert len(game.children) == 0


def test_draw_functions_and_order():
    """
    Validates that draw functions are called in the order they are added.
    This also ensures that the surface is passed correctly.
    """
    called: list[str] = []
    surface = None

    def draw_1(value):
        nonlocal surface
        surface = value
        called.append("draw_1")

    def draw_2(value):
        nonlocal surface
        surface = value
        called.append("draw_2")

    def draw_3(value):
        nonlocal surface
        surface = value
        called.append("draw_3")

    game = Game()
    game.add_draw_func(draw_1)

    game.draw("fred")
    assert called == ["draw_1"]
    assert surface == "fred"

    called.clear()

    game.add_draw_func(draw_2)
    game.add_draw_func(draw_3)

    game.draw("scooby")
    assert called == ["draw_1", "draw_2", "draw_3"]
    assert surface == "scooby"


def test_update_functions_and_order():
    """
    Validates that update functions are called in the order they are added.
    This also ensures that dt is passed correctly.
    """
    called: list[str] = []
    dt = None

    def update_1(value):
        nonlocal dt
        dt = value
        called.append("update_1")

    def update_2(value):
        nonlocal dt
        dt = value
        called.append("update_2")

    def update_3(value):
        nonlocal dt
        dt = value
        called.append("update_3")

    game = Game()
    game.add_update_func(update_1)

    game.update(0.1)
    assert called == ["update_1"]
    assert dt == 0.1

    called.clear()

    game.add_update_func(update_2)
    game.add_update_func(update_3)

    game.update(0.3)
    assert called == ["update_1", "update_2", "update_3"]
    assert dt == 0.3


def test_root_gets_drawn():
    """
    Validates that the root object gets drawn and is passed the correct values.
    """
    called: list[str] = []
    surface = None
    that = None

    def draw_root(this, value):
        nonlocal surface, that
        surface = value
        that = this
        called.append("draw_root")

    game = Game()
    game.root.add_draw_handler(draw_root)

    game.draw("thelma")
    assert called == ["draw_root"]
    assert surface == "thelma"
    assert that == game.root


def test_root_gets_updated():
    """
    Validates that the root object gets updated and is passed the correct values.
    """
    called: list[str] = []
    dt = None
    that = None

    def update_root(this, value):
        nonlocal dt, that
        dt = value
        that = this
        called.append("update_root")

    game = Game()
    game.root.add_update_handler(update_root)

    game.update(0.3)
    assert called == ["update_root"]
    assert dt == 0.3
    assert that == game.root


def test_root_drawn_before_draw_funcs():
    """
    Validates that the root GameObject is drawn before draw functions are called.
    """
    called: list[str] = []

    def draw_1(value):
        called.append("draw_1")

    def draw_2(value):
        called.append("draw_2")

    def draw_root(this, value):
        called.append("draw_root")

    game = Game()
    game.add_draw_func(draw_1)
    game.root.add_draw_handler(draw_root)
    game.add_draw_func(draw_2)

    game.draw("shaggy")
    assert called == ["draw_root", "draw_1", "draw_2"]


def test_root_updated_before_update_funcs():
    """
    Validates that the root GameObject is updated before update functions are called.
    """
    called: list[str] = []

    def update_1(value):
        called.append("update_1")

    def update_2(value):
        called.append("update_2")

    def update_root(this, value):
        called.append("update_root")

    game = Game()
    game.add_update_func(update_1)
    game.root.add_update_handler(update_root)
    game.add_update_func(update_2)

    game.update(0.1)
    assert called == ["update_root", "update_1", "update_2"]


def test_properties_passed_to_execute():
    """
    Validates that the correct properties are passed to the execute function.
    """
    game = Game()
    expected_size = None
    expected_bgc = None

    def execute(g, bgc: tuple[int, int, int] = None):
        assert g == game
        expected_width, expected_height = expected_size

        assert g.width == expected_width
        assert g.height == expected_height

        assert expected_bgc == bgc

    # This is naughty as a lot could go wrong so we must make sure we restore the execute function.
    import pmpge.game as my_game
    original_execute = my_game.execute
    try:
        my_game.execute = execute

        game = Game()
        expected_size = (640, 480)
        expected_bgc = (0, 0, 0)
        game.run()

        game = Game(320, 240, background_color=(1, 2, 3))
        expected_size = (320, 240)
        expected_bgc = (1, 2, 3)
        game.run()

        game = Game(800, 300, background_color=(5, 4, 7))
        expected_size = (800, 300)
        expected_bgc = (5, 4, 7)
        game.run()

    finally:
        my_game.execute = original_execute


def test_run_and_terminate():
    """
    Validates that run and terminate work, simply by executing them. This also ensure that
    the update() and draw() methods are called.
    """

    update_counter = 0

    def update(dt: float):
        nonlocal update_counter
        update_counter += 1
        if update_counter >= 10:
            game.terminate()

    draw_counter = 0

    def draw(dt: float):
        nonlocal draw_counter
        draw_counter += 1

    game = Game()
    game.add_update_func(update)
    game.add_draw_func(draw)

    game.run()

    assert update_counter == 10
    assert draw_counter == 10
