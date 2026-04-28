# Optimisation

This file contains the information about what optimisations are being
investigated and what has already been done.

## Reference test hardware

All performance testing has been done on the following devices using a mix
of microcontrollers to compare performance. All testing was done using
CircuitPython 10.1.4 using the following `config.py` except where a specific
`config.py` file is provided:

```
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128
RUNTIME = 2
SAMPLE_FREQUENCY = 50
REPORT_FREQUENCY = 4
PROFILE = True
PROFILE_TOP = 10
```

### Plain boards: No screens, buttons or buzzers

* Raspberry Pi Pico running (Pico)
* Raspberry Pi Pico 2 running (Pico 2)
* Waveshare S3 Zero running
* Itsy Bitsy M4 Express (ATSAMD51)

### Rich boards: With screens, buttons, buzzers

* Desktop PC (for comparison)
* Pico System (Pico)
* Adafruit EdgeBadge (ATSAMD51)

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

Use the following method to flash the Pico system:

1. Turn your PicoSystem off.
2. Hold down the X button.
3. While holding X, turn on the device or connect it to your computer via USB.

The following references have been used:

* [10 Smart Performance Hacks For Faster Python Code](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)
* [Embedded Python: Cranking Performance Knob up to Eleven!](https://urish.medium.com/embedded-python-cranking-performance-knob-up-to-eleven-df31a5940a63)
* [Maximising MicroPython speed](https://docs.micropython.org/en/latest/reference/speed_python.html)
* [Performance Limitations of CircuitPython's DisplayIO Graphics](https://joshondesign.com/2023/06/12/display_io_perf)
