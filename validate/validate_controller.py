import validate.controller.move_sprite as fms
import validate.utils as utils

modules = [fms]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
