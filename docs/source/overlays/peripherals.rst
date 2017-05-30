Peripherals & Interfaces
=============

Peripherals
-----------

Typical embedded systems support a fixed configuration of peripherals (e.g. SPI, IIC, UART, Video, USB etc.). They may also have some GPIO available to interface to custom hardware, but typically the number of GPIO will be limited, and as the GPIO are controlled from the main CPU, performance is usually limited. 

Zynq platforms typically have many more pins available to extend the system, and as hardware controllers and additional soft processors can be implemented in the PL, performance can be much higher than a typical embedded system. 

PYNQ runs on Linux and the following Zynq PS peripherals are required by default: SD Card to boot the system, and Linux filesystem, Ethernet to connect to Jupyter notebook, UART for linux terminal access, and USB. On most Zynq platforms these peripherals are connected to the Zynq PS. 

The USB port and other standard interfaces can also be used to connect off-the-shelf USB and other peripherals to the Zynq PS. Linux drivers are required for connecting USB peripherals. The PYNQ image currently includes drivers for the most commonly used USB webcams, wifi peripherals, and other standard USB devices.

Other peripherals are usually connected to the Zynq PL. E.g. HDMI, Audio, Buttons, Switches, LEDs, and general purpose interfaces including Pmods, and Arduino. An overlay which provides controllers for these peripherals or interfaces is required before they can be used. 

A library of hardware IP for standard and specialized peripherals is included in Vivado. PYNQ provides a Python API for a number of common peripherals including HDMI in and Out, Buttonns, Switches, LEDs, and can be extended to support additional IP. 

Note that only a limited number of the dedicated Zynq PS peripherals (Ethernet, USB, UART, IIC, SPI, CAN controllers and GPIO) can be connected externally on a Zynq development board; typically SD card, Ethernet, USB, and UART. It is possible to connect some of the other dedicated peripherals internally to the Zynq PL. The peripherals could then be used internally inside the PL, or routed to PL pins. E.g. to Pmod, or Arduino pins. 

Interfaces
---------------

Zynq platforms usually have one or more headers that allow connection of external peripherals. The Pmod and Arduino interface are commonly used on Zynq development boards to allow standard peripherals to be connected to the PL. Other peripherals can be connected to these ports via adapters, or with a breadboard. Note that while a peripheral can be physically connected to the Zynq PL pins, a controller must be built into the overlay before the peripheral can be used. 


Pmod port
^^^^^^^^^^^^^^^^^^

A Pmod port is an open 12-pin interface that is supported by a range of Pmod peripherals from Digilent and third party manufacturers. 
Typical Pmod peripherals include sensors (voltage, light, temperature), communication interfaces (Ethernet, serial, wifi, bluetooth), and input and output interfaces (buttons, switches, LEDs).


.. image:: ../images/pynqz1_pmod_interface.jpg
   :align: center


Pmod pins
^^^^^^^^^^^^^^^^

Each Pmod connector has 12 pins arranged in 2 rows of 6 pins. Each row has 3.3V (VCC), ground (GND) and 4 data pins. Using both rows gives 8 data pins in total. 

Pmods come in different configurations depending on the number of data pins required. e.g. Full single row: 1x6 pins; full double row: 2x6 pins; and partially populated: 2x4 pins. 

.. image:: images/pmod_pins.png
   :align: center

Pmods that use both rows (e.g. 2x4 pins, 2x6 pins), should usually be aligned to the left of the connector (to align with VCC and GND). VCC and GND are labelled on the PYNQ-Z1 board. 

.. image:: images/pmod_tmp2_8pin.JPG

Pmod peripherals with only a single row of pins can be connected to either the top row or the bottom row of a Pmod port (again, aligned to VCC/GND). If you are using an existing driver/overlay, you will need to check which pins/rows are supported for a given overlay, as not all options may be implemented. e.g. the Pmod ALS is currently only supported on the top row of a Pmod port, not the bottom row.  

Pmod IO standard
^^^^^^^^^^^^^^^^^^^^^^^^^^

All pins operate at 3.3V. Due to different pull-up/pull-down I/O requirements for different peripherals (e.g. IIC requires pull-up, and SPI requires pull-down) the Pmod data pins have different IO standards. 

0,1 and 4,5 are connected to pins with pull-down resistors. This can support the SPI interface, and most peripherals. 2,3 and 6,7 are connected to pins with pull-up resistors. This can support the IIC interface. 

Pmods already take this pull up/down convention into account in their pin layout, so no special attention is required when using Pmods. 
   

Other Peripherals
-----------------------------

Pmod ports are design for use with Pmods. The 8 data pins of a Pmod port can be used to connect to a breadboard, or directly to other peripherals. 

Grove peripherals which use a four wire interface can also be connected to the Pmod port through a *PYNQ Grove Adapter*.


PYNQ Grove Adapter
^^^^^^^^^^^^^^^^^^^

A Grove connector has four pins, VCC and GND, and two data pins.

The PYNQ Grove Adapter has four connectors (G1 - G4), allowing up to four Grove devices to be connected to one Pmod port. Remember that an IOP application will be required to support the configuration of connected peripherals.

.. image:: ../images/pmod_grove_adapter.jpg
   :align: center

Pmod IO standard for Grove
^^^^^^^^^^^^^^^^^^^^^^^^^^^

On the grove adapter G1 and G2 map to Pmod pins [0,4] and [1,5], which are connected to pins with pull-down resistors (supports SPI interface, and most peripherals). G3 and G4 map to pins [2,6], [3,7], which are connected to pins with pull-up resistors (IIC), as indicated in the image. 

.. image:: ../images/adapter_mapping.JPG
   :align: center
   

Arduino connector
-----------------------

There is one Arduino connector on the board and can be used to connect to Arduino compatible shields. 

.. image:: ../images/pynqz1_arduino_interface.jpg
   :align: center

Arduino pins
^^^^^^^^^^^^^^^^^^^^^^^^^

Each Arduino connector has 6 analog pins (A0 - A5), 14 multi-purpose Digital pins (D0 - D13), 2 dedicated I2C pins (SCL, SDA), and 4 dedicated SPI pins. 

Supported Arduino shields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arduino standard supports 5V on all pins, including analog pins. Most Arduino compatible shields can be used with a PYNQ, but as Zynq analog pins only support 1V peak-to-peak, some analog shields may not work without additional interfacing circuitry. 


Using Pmod and Arduino Peripherals
-----------------------------------------

Pynq introduces IOPs (Input Output Processors) which are covered in the next section. An IOP consists of a MicroBlaze processor with dedicated peripherals which can be selected and routed to the physical interface at runtime. An IOP provides flexibility allowing peripherals with different protocols and interfaces to be used with the same overlay. 
A peripheral will have an IOP driver application, and a Python wrapper. The next sections will cover the IOP architecture, and how to write driver applications and the corresponding Python wrapper for a peripheral. 


