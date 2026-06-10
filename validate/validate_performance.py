import validate.performance.baseline as baseline
import validate.performance.baseline_with_graphics as with_graphics
import validate.performance.baseline_with_graphics_small_display as small_display
import validate.performance.huge_hierarchy as hh
import validate.utils as utils

modules = [baseline, with_graphics, small_display, hh]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
