import validate_device.engine.game_objects_with_traits as got
import validate_device.engine.hierarchy_with_traits as hwt
import validate_device.engine.just_game_objects as jgo
import validate_device.engine.trivial_game as tg
import validate_device.utils as utils

modules = [tg, jgo, got, hwt]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
