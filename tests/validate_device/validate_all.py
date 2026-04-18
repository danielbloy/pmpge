import tests.validate_device.helper as helper
import tests.validate_device.validate_a_core as a
import tests.validate_device.validate_b_memory as b

modules = [a, b]


def execute():
    helper.report_memory_usage()
    for module in modules:
        print("Executing module {}".format(module))
        module.execute()
        helper.report_memory_usage_and_free()
        del module


if helper.should_execute(__name__):
    execute()
