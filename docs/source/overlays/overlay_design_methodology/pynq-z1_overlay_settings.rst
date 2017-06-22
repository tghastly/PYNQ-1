******************************
PYNQ-Z1 Base overlay settings
******************************

Base overlay project
=======================

It is recommended to start with an existing overlay design to ensure the PS settings are correct. The source files for the *base* overlay can be found in the PYNQ GitHub. The project can be rebuilt using the makefile/TCL available here:
   
   ``<GitHub repository>/boards/<board name>/vivado/base``


Vivado Project settings
=========================

The following settings should be used for a new Vivado overlay project for the PYNQ-Z1: 

* Target device: xc7z020clg400-1

PL clock configuration:

* FCLK_CLK0: 100.00 MHz
* FCLK_CLK1: 142.86 MHz
* FCLK_CLK2: 200.00 MHz
* FCLK_CLK3: 100 MHz

If any other clock settings are required, they must be configured from Python before the new overlay is downloaded. All clocks should be restored to the base settings before another overlay is loaded. 

Pynq-Z1 Constraints file
============================

The PYNQ-Z1 Master XDC (I/O constraints) are available at the Digilent PYNQ-Z1 resource site:
https://reference.digilentinc.com/reference/programmable-logic/boards/<board name>/start

