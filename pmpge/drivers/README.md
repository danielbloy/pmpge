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

There are other configuration properties that can be set to control the behaviour
of the framework:

* `UPDATE_FRAMERATE` - Only applies to microcontrollers, not Pygame Zero. Sets the
  rate limit for the `update()` calls. If not set, the default will be 60 fps.
* `GRAPHICS_FRAMERATE` - Only applies to microcontrollers, not Pygame Zero. Sets the
  rate limit for the `draw()` calls. If not set, the default will be 30 fps.
* `GRAPHICS_STATS` - Only applies to microcontrollers, not Pygame Zero. If set to True
  the game will display graphics stats along the bottom of the screen. If not set, the
  default will be False.
* `GRAPHICS_SCALING` - Only applies to microcontrollers, not Pygame Zero. Enforces a
  scaling factor for the graphics. Typically used to stop small displays such as
  160 x 120 from being upscaled on larger screens.
* `GRAPHICS_MANUAL_REFRESH` - Only applies to microcontrollers, not Pygame Zero. If set,
  the game will manually control the refresh rate (as opposed to automatically) to the
  desired rate set by the `GRAPHICS_FRAMERATE` configuration property.
* `CONTROLLER_CLOCK`, `CONTROLLER_OUT`, `CONTROLLER_LATCH`, `CONTROLLER_MAPPING` - Only
  applies to microcontrollers, not Pygame Zero. Used to configure a controller that
  uses a shift register to read button states. See the shift register controller device
  driver for more details.
* `CONTROLLER_PULLUP` - Only applies to microcontrollers, not Pygame Zero. Used when the
  controller buttons are directly connected to microcontroller pins. Used to specify if
  the buttons use pullup resistors or not. If not set, the default value will be True.
* `CONTROLLER_START`, `CONTROLLER_A` etc. - Only applies to microcontrollers, not Pygame
  Zero. Used to specif which pin each controller button is connected to. There is a
  configuration value for each of the buttons. Buttons that are not provided values are
  assumed to not be present on the controller. See the pins controller device driver for
  more details.

## Implementing a driver

Implementing a driver is pretty simple for the most part. There are
optional common hook methods for all drivers and mandatory methods
or classes that must be implemented for specific drivers. The optional
methods are:

* `init()` - called once when the game first runs.
    * The screen variant of `init()` accepts 5 parameters:
        * `game` - the Game object that is being executed.
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
