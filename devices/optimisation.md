# Optimisation

This file contains the information about what optimisations are being
investigated and what has already been done.

## Reference test hardware

All performance testing has been done on a Adafruit EdgeBadge running CircuitPython 10.1.4.

The tests executed is the code found in `tests/validate_device`

## Optimisation results

* a = `validate_a_core.py`
* b = `validate_b_memory.py`

Initial:

* a = 405.80 updates per second
* b = 17.80 updates per second

```
Running on circuit with (60, 20) screen and 0 button controller.
Peak: 17584 bytes, Used: 17584 bytes, Free: 127824 bytes
Peak: 63360 bytes, Used: 37872 bytes, Free: 107536 bytes
Peak: 63488 bytes, Used: 56512 bytes, Free: 88896 bytes
Peak: 63488 bytes, Used: 30176 bytes, Free: 115232 bytes
Peak: 63488 bytes, Used: 49472 bytes, Free: 95936 bytes
Peak: 63488 bytes, Used: 22176 bytes, Free: 123232 bytes
Peak: 63488 bytes, Used: 42112 bytes, Free: 103296 bytes
Peak: 63488 bytes, Used: 60656 bytes, Free: 84752 bytes
Peak: 63488 bytes, Used: 34592 bytes, Free: 110816 bytes
Peak: 63488 bytes, Used: 53616 bytes, Free: 91792 bytes
Achieved 405.80 update cycles per second
Peak: 63488 bytes, Used: 24704 bytes, Free: 120704 bytes
```

### Checking RAM allocations

Using dynamic heap memory is fast so initial optimisations are looking at the `Game` and
`GameObject` classes plus the main event loop to minimise dynamic memory usage.

Vanilla results:

## Optimisation roadmap

* Replace all `float` based maths with `int` by changing units from pixels per second to thousandth pixels per second

### References

The following references have been used:

* [10 Smart Performance Hacks For Faster Python Code](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)
* [Embedded Python: Cranking Performance Knob up to Eleven!](https://urish.medium.com/embedded-python-cranking-performance-knob-up-to-eleven-df31a5940a63)
* [Maximising MicroPython speed](https://docs.micropython.org/en/latest/reference/speed_python.html)
* [Performance Limitations of CircuitPython's DisplayIO Graphics](https://joshondesign.com/2023/06/12/display_io_perf)
