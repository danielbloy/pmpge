import tests.validate_device.utils as utils

modules = []

if utils.should_execute(__name__):
    utils.execute_modules(modules)
