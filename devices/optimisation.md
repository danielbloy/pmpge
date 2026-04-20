# Optimisation

This file contains the information about what optimisations are being
investigated and what has already been done.

## Reference test hardware

All performance testing has been done on the following devices:

* Desktop PC
* Adafruit EdgeBadge running CircuitPython 10.1.4.
* Raspberry Pi Pico running CircuitPython 10.1.4.
* Raspberry Pi Pico 2 running CircuitPython 10.1.4.
* Waveshare S3 Zero running CircuitPython 10.1.4.

Using the following `config.py`

```
SCREEN_WIDTH = 1
SCREEN_HEIGHT = 1
RUNTIME = 2
SAMPLE_FREQUENCY = 50
REPORT_FREQUENCY = 4
PROFILE = True
PROFILE_TOP = 10
```

The tests executed is the code found in `tests/validate_device`

## Optimisation results

See the directory `results` for the latest results. Check the history of the files to
see how the optimisation process has progressed.

### Checking RAM allocations

Using dynamic heap memory is fast so initial optimisations are looking at the `Game` and
`GameObject` classes plus the main event loop to minimise dynamic memory usage.

Vanilla results:

## Optimisation roadmap

* Replace all `float` based maths with `int` by changing units from pixels per second to thousandth pixels per second

### References

Use the following tool to program the Waveshare ESP-S3 Zero:

* https://learn.adafruit.com/circuitpython-with-esp32-quick-start/web-serial-esptool

The following references have been used:

* [10 Smart Performance Hacks For Faster Python Code](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)
* [Embedded Python: Cranking Performance Knob up to Eleven!](https://urish.medium.com/embedded-python-cranking-performance-knob-up-to-eleven-df31a5940a63)
* [Maximising MicroPython speed](https://docs.micropython.org/en/latest/reference/speed_python.html)
* [Performance Limitations of CircuitPython's DisplayIO Graphics](https://joshondesign.com/2023/06/12/display_io_perf)
