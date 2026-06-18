# This script runs all the validation tests. It is a convenient way to
# test a large subset of the functionality on a single device.

import validate.utils as utils
import validate.validate_controller as controller
import validate.validate_engine as engine
import validate.validate_graphics as graphics
import validate.validate_performance as performance
import validate.validate_sound as sound

scripts = [controller, engine, graphics, sound, performance]

if utils.should_execute(__name__):
    for script in scripts:
        modules = script.modules
        utils.execute_modules(modules)
