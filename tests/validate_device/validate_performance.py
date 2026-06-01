import tests.validate_device.performance.huge_hierarchy as hh
import tests.validate_device.utils as utils

modules = [hh]

# TODO: A test using a 80 x 100 display for performance.

if utils.should_execute(__name__):
    utils.execute_modules(modules)
