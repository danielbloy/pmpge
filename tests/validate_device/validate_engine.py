import tests.validate_device.engine.game as a
import tests.validate_device.engine.game_object as b
import tests.validate_device.engine.hierarchy as c
import tests.validate_device.engine.traits as d
import tests.validate_device.engine.traits_simple as ds
import tests.validate_device.utils as utils

modules = [a, b, c, ds, d]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
