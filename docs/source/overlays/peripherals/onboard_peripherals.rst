Onboard GPIO Peripherals
=========================

Zynq boards usually include basic onboard peripherals including buttons, switches, and LEDs. These peripherals are usually connected to the Zynq PL and controlled using an AXI GPIO controller in an overlay. It is also possible to build an overlay which connects these perpherals to the Zynq PS GPIO controller. 

PYNQ provides an ''AxiGPIO'' class to control GPIO. It provides ''read()'' and ''write()'' functions. 

The GPIO class is extended by the ''Button'', ''Swtich'', ''LED'' and ''RGBLED'' classes for the corresponding peripherals on a board. 

GPIO peripherals are supported in the base overlay. 



