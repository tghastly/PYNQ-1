***********************
Overlay Design
***********************

.. contents:: Table of Contents
   :depth: 2
   

Overlay design
=======================

An overlay consists of two main parts; the PL design (bitstream) and the project block diagram TCL file. This section assumes the reader has some experience with Zynq, and the Vivado design tools. 


Block Diagram TCL
--------------------

The block diagram TCL can be used by PYNQ to automatically identify the Zynq system configuration, IP in an overlay and their versions, interrupts, resets, and other control signals. Based on this information, the system configuration can be modified, drivers can be automatically assigned, features can be enabled or disabled, and signals can be connected to corresponding Python functions. 

The TCL file can be generated in Vivado by *exporting* the IP Integrator block diagram at the end of the overlay design process. The .tcl should be provided with a bitstream when downloading an overlay. The PYNQ PL class will automatically parse the TCL. 

A custom, or manually created TCL file can be used to build a Vivado project, but Vivado should be used to generate and export the TCL file for the block diagram. This automatically generated TCL should ensure that it can be parsed correctly. 

PL Design
------------------

The Xilinx® Vivado software is used to create a Zynq design. A *bitstream* or *binary* file (.bit file) will be generated that can be used to program the Zynq PL.

A free WebPack version of Vivado is available to build overlays.
https://www.xilinx.com/products/design-tools/vivado/vivado-webpack.html

Programmability
^^^^^^^^^^^^^^^^^

An overlay should have post-bitstream programmability to allow customization of the system. A number of reusable PYNQ IP blocks are available to support programmability. For example, an IOP can be used on Pmod, and Arduino interfaces. IP from the PYNQ DIO overlay can be reused to provide run-time configurability. 

See the previous section on `PYNQ IP <../pynq_ip_index.html>'_

Zynq PS settings
^^^^^^^^^^^^^^^^^^^^^

A Vivado project for a Zynq design consists of two parts; the PL design, and the PS configuration settings. 

The PYNQ image which is used to boot the board configures the Zynq PS at boot time. This will fix most of the PS configuration, including setup of DRAM, and enabling of the ZYnq PS peripherals, including SD card, Ethernet, USB and UART which are used by PYNQ. 

The PS configuration also includes settings for system clocks, including the clocks used in the PL. The PL clocks can be programmed at runtime to match the requirements of the overlay. This is managed automatically by the PYNQ Overlay class. 

During the process of downloading a new overlay, the clock configuration will be parsed from the overlay's .tcl file. The new clock settings for the overlay will be applied automatically before the overlay is downloaded. 



Generate overlay TCL file
------------------------------

To generate the TCL for the Block Diagram from the Vivado GUI:

   * Click **File > Export > Block Design**  

Or, run the following in the tcl console:

.. code-block:: console

   write_bd_tcl
      
The tcl filename should match the .bit filename. E.g. my_overlay.bit and my_overlay.tcl

The tcl is parsed when the overlay is instantiated and downloaded. 

.. code-block:: python

   from pynq import Overlay
   ol = Overlay("base.bit") # tcl is parsed here

   
An error will be displayed if a tcl is not available when attempting to download an overlay, or if the tcl filename does not match the .bit file name.


Existing Overlays
=========================

Existing overlays can be used as a starting point to create a new overlay. The *base* overlay can be found in the boards directory in the Pynq repository, and includes reference IP for peripherals on the board: 

   ``<GitHub repository>/boards/<board name>/vivado/base``
  
A makefile exists in each folder that can be used to rebuild the Vivado project and generate the bitstream and TCL for the overlay. (On windows, instead of using *make*, the .tcl can be sourced from Vivado.)

The bitstream and tcl for the overlay are available on the board, and also in the GitHub project repository: 

   ``<GitHub Repository>/boards/<board name>/bitstream/``

