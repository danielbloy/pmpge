# Devices

By default, the implementation of `pmpge` is designed to make it as simple as
possible to write games for Pygame Zero which already provides a complete
platform abstraction. However, a stretch goal is to also extend the framework to
work on common microcontrollers. The aim of supporting these devices is for
users of this framework (typically expected to be Code Clubs) to not need to
make any changes to simply run their games on one of the reference hardware
devices. Before getting too carried away, Python is vastly slower and C/C++,
Golang or even the MakeCode platform so we need to be realistic about what we
are aiming for here. The goal is to be able to achieve the following levels
of performance to run relatively simple games on these microcontrollers:

* 30 fps at a resolution of 160 x 120 pixels (no scaling)
* 20 to 50 GameObjects with a small number of traits each
* 8 x 8 or 16 x 16 pixel sprites
* Simple collision detection
* A background layer with limited scrolling.

As well as which devices are supported, this section also contains the
information on the optimisation that is done or being investigated to improve
the performance on the microcontroller based boards. Making the microcontroller
implementation faster also has positive benefits on normal computers.

Naturally, RAM and CPU resources are much more limited on these tiny devices and
the display resolution is much lower. Typically these devices will have screens
with a resolution of:

* 160 x 128 pixels
* 240 x 240 pixels
* 320 x 240 pixels
* 640 x 480 pixels

_**NOTE:** Please be aware that the initial releases of PMPGE are validated
for functionality and ease of use rather than optimisation for performance on
small devices. Optimisation will always come after working functionality._

For information on optimisations, see the files [optimisation.md](./optimisation.md).

## Supporting CircuitPython and MicroPython

The project aims to support both CircuitPython and MicoPython, though doing so by
utilising a specific set of libraries on each target hardware. Support is added
first for CircuitPython as that is what I use most in my Code Clubs. MicroPython
will follow afterwards.

### CircuitPython

On CircuitPython, where devices support the `Stage` and `ugame` libraries, they will
be used. Otherwise, the supported display driver is to use `displayio`.

* [CircuitPython Display Support Using displayio](
  https://learn.adafruit.com/circuitpython-display-support-using-displayio/introduction)
* [displayio – High level, display object compositing system](
  https://docs.circuitpython.org/en/latest/shared-bindings/displayio/)

### MicroPython

On MicroPython, the supported display driver is to use pico-graphics:

* [Pico Graphics](
  https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md)

### Raspberry Pi with additional SPI screen/controller

For an interesting diversion, another aim is to be able to support a Raspberry Pi using
an additional SPI connected display. There are many HATs out there with screen and buttons
such as this one:

* [Raspberry Pi HAT](
  https://www.amazon.co.uk/dp/B0DQXYJY4X?ref=cm_sw_r_cso_em_mwn_dp_BK5HK79X16XEKVJW77Z4&social_share=cm_sw_r_cso_em_mwn_dp_BK5HK79X16XEKVJW77Z4)

## Reference hardware

The following are commercial hardware devices that will be used to test the framework:

* Adafruit [PyBadge](https://www.adafruit.com/product/4200) for CircuitPython only. This is the device that will also
  be used for the majority of the early microcontroller implementation and
  optimisations.
* Pimoroni [PicoSystem](https://shop.pimoroni.com/products/picosystem?variant=32369546985555)
  for CircuiPython and MicroPython

Additionally, I will make two reference systems using COTS parts using:

Design 1:

* Raspberry Pi Pico 2
* Generic ST7735R 160 x 128 pixel display
* 8 x Standard push buttons

Design 2:

* Pimoroni [Pico Plus 2](
  https://shop.pimoroni.com/products/pimoroni-pico-plus-2?variant=42092668289107)
* Pimoroni [Pico Display 2.8"](
  https://shop.pimoroni.com/products/pico-display-pack-2-8?variant=42047194005587)

* 8 x Standard push buttons
