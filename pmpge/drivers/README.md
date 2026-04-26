# Drivers

This documentation will describe what is needed to implement a driver
for `pmpge`. There are four drivers that can be implemented. Each has
a default driver based on the environment it is executing in but this
can be overridden by setting a configuration property. The four types
of driver and their configuration properties are:

* `DEVICE_DRIVER`
* `CONTROLLER_DRIVER`
* `SOUND_DRIVER`
* `GRAPHICS_DRIVER`

Implementing a driver is pretty simple for the most part. There are
optional common hook methods for all drivers and mandatory methods
or classes that must be implemented for specific drivers. The optional
methods are:

* `init()` - called once when the game first runs.
    * The screen variant of `init()` accepts 5 parameters:
        * `width` - the width of the game in pixels.
        * `height` - the height of the game in pixels.
        * `screen_width` - the width of the screen in pixels.
        * `screen_height` - the height of the screen in pixels.
        * `background_colour` - the default colour of the background in RGB format.
* `update(delta_time: float)` - called once every update cycle before anything else.
* `deinit()` - called once when the game finishes.

For details on the mandatory implementations, see the relevant subpages:

* [`DEVICE_DRIVER`](device.md)
* [`CONTROLLER_DRIVER`](controller.md)
* [`SOUND_DRIVER`](sound.md)
* [`GRAPHICS_DRIVER`](graphics.md)
