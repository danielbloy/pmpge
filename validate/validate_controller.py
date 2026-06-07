import validate_device.controller.move_sprite as fms

import validate_device.utils as utils

modules = [fms]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
