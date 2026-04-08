import pmpge.environment as environment


def test_report():
    """
    Simply tests there is no error calling the report method.
    """
    environment.report()


def test_controller_or_desktop():
    """
    Just a simple test to make sure we are not returning a microcontroller and desktop environment
    """
    assert environment.is_running_on_desktop() != environment.is_running_on_microcontroller()


def test_config_is_loaded() -> None:
    """
    Validates configuration defaults are loaded as well as the local overrides
    contained in config.py.
    """

    # These are just random configuration values from the config.
    # noinspection PyUnresolvedReferences
    assert environment.TEST_VALUE == 123.456
    assert environment.TEST_STRING == "Hello world!"


def test_system():
    """
    Validates that the system is the default value which is "pgzero".
    """
    assert environment.system() == "pgzero"

# TODO: Test the following functions:
#   * is_running_on_circuitpython()
#   * is_running_on micropython()
#   * get_controller_driver()
#   * get_device_driver()
#   * get_graphics_driver()
#   * get_sound_driver()
#   * screen_size()
#   * system()
#   * termiante()
#   * execute()
