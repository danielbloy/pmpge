import tests.validate_device.utils as utils
import tests.validate_device.validate_a_core as a
import tests.validate_device.validate_b_memory as b

modules = [a, b]


def execute():
    for module in modules:
        print("Executing module {}".format(module))
        utils.execute(module.setup)
        del module


if utils.should_execute(__name__):
    execute()
