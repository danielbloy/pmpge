# This script runs all the validation tests that are not interactive.
# It is a convenient way to test a large subset of the functionality
# on a device.
#
import tests.validate_device.engine.game_objects_with_traits as got
import tests.validate_device.engine.hierarchy_with_traits as hwt
import tests.validate_device.engine.just_game_objects as jgo
import tests.validate_device.engine.trivial_game as tg
import tests.validate_device.utils as utils

modules = [tg, jgo, got, hwt]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
