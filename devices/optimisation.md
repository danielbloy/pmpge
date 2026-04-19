# Optimisation

This file contains the information about what optimisations are being
investigated and what has already been done.

## Reference test hardware

All performance testing has been done on a Adafruit EdgeBadge running CircuitPython 10.1.4.

The tests executed is the code found in `tests/validate_device`

## Optimisation results

## Optimisation roadmap

* Replace all `float` based maths with `int` by changing units from pixels per second to thousandth pixels per second

### References

The following references have been used:

* [10 Smart Performance Hacks For Faster Python Code](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)
* [Embedded Python: Cranking Performance Knob up to Eleven!](https://urish.medium.com/embedded-python-cranking-performance-knob-up-to-eleven-df31a5940a63)
* [Maximising MicroPython speed](https://docs.micropython.org/en/latest/reference/speed_python.html)
* [Performance Limitations of CircuitPython's DisplayIO Graphics](https://joshondesign.com/2023/06/12/display_io_perf)
