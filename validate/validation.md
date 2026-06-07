# Validating on a device

The validation scripts are designed to be run on a CircuitPython device to
validate both the performance of PMPGE but also validate the correct behaviour
of the drivers as these are impossible to test on a PC with automated testing.
Some of the validation tests require a human to check the results so have some
interactivity. There is also a `validate_all.py` script which runs all the
non-interactive tests.

The following steps are required to be followed to run the validation
on a CircuitPython device.

1. Copy the entire `pmpge` directory to the root of the device.
2. Copy the entire `validate` directory in the root of the device.
3. Create a `images` directory in the root of the device.
4. Copy all Python files from `validate/images` into the
   `images` directory on the device.
5. Create a `lib` directory in the root of the device.
6. Copy across the contents of `validate/lib` into the `lib`
   directory on the device.
7. Use Thonny to run one of the validate scripts such as`validate_performance.py`.

# TODO: How to setup the config.py files.
