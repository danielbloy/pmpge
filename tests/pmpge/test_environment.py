import pmpge.environment as environment


class TestEnvironment:
    def test_report(self):
        """
        Simply tests there is no error calling the report method.
        """
        environment.report()

    def test_controller_or_desktop(self):
        """
        Just a simple test to make sure we are not returning a microcontroller and desktop environment
        """
        assert environment.is_running_on_desktop() != environment.is_running_on_microcontroller()

    def test_config_is_loaded(self) -> None:
        """
        Validates configuration defaults are loaded as well as the local overrides
        contained in config.py.
        """

        # These are just random configuration values from the config.
        # noinspection PyUnresolvedReferences
        assert environment.TEST_VALUE == 123.456
        assert environment.TEST_STRING == "Hello world!"

    def test_system(self):
        """
        Validates that the system is the default value which is "pgzero".
        """
        assert environment.system() == "pgzero"

# TODO: Test the following functions:
#   * is_running_on_circuitpython()
#   * is_running_on micropython()
#   * is_python()
#   * get_controller_driver()
#   * get_device_driver()
#   * get_graphics_driver()
#   * get_sound_driver()
#   * get_system_driver()
#   * get_driver()
