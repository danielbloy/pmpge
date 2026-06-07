import validate_device.performance.baseline as baseline
import validate_device.performance.baseline_with_graphics as with_graphics
import validate_device.performance.baseline_with_graphics_small_display as small_display
import validate_device.performance.huge_hierarchy as hh
import validate_device.utils as utils

modules = [baseline, with_graphics, small_display, hh]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
