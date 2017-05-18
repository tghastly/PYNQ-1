*****************
PYNQ image build 
*****************

.. contents:: Table of Contents
   :depth: 2
 
This section documents the process of building the PYNQ image for the PYNQ-Z1. 


Overview

=================

The PYNQ image is built using a custom make flow. 

Components
=================

Boot files
PYNQ package (includes overlays)

Sources
=================

device tree
PYNQ package


Retargeting to a different board
==================================

The main differences between different PYNQ boards are related to the memory, and the peripherals that are conected to the Zynq device. 

For the memory, you will need to define the specific memory part used on the target board. This can be done in the Vivado IPI GUI, and is part of the standard Zynq design process. If a board support package is available, this can be used to generate the base Zynq configuration for the target board. 

Once the base system settings have been defined, a device tree is required. The existing device tree can be modified to match the new board.  