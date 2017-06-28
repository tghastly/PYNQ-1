Onboard Peripherals
=====================

Zynq platforms usually include basic onboard peripherals including buttons, switches, and LEDs. These peripherals are usually connected to the Zynq PL and controlled using a GPIO controller in an overlay. It is also possible to build an overlay which connects these perpherals to the Zynq PS GPIO controller. 

PYNQ provides a Python ''GPIO'' class which allows the direction of the GPIO to be set (input or output), and ''read()'' and ''write()'' functions. 

The GPIO class is extended by the ''Button'', ''Swtich'', ''LED'' and ''RGBLED'' classes for the corresponding peripherals on a board. 

GPIO peripherals are supported in the base overlay. 



