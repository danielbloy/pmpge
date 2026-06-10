import validate.engine.game_objects_with_traits as got
import validate.engine.hierarchy_with_traits as hwt
import validate.engine.just_game_objects as jgo
import validate.engine.trivial_game as tg
import validate.utils as utils

modules = [tg, jgo, got, hwt]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
