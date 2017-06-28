**********************
Creating Overlays
**********************

.. contents:: Table of Contents
   :depth: 2
   
Introduction 
=============

As described in the PYNQ introduction, overlays are analogous to software libraries. A programmer can download overlays into the Zynq® PL at runtime to provide functionality required by the software application. 

An *overlay* is a class of Programmable Logic design. Programmable Logic designs are usually highly optimized for a specific task. Overlays however, are designed to be configurable, and reusable for broad set of applications. A PYNQ overlay will have a Python interface, allowing a software programmer to use it like any other Python package. 

A software programmer can use an overlay, but will not usually create overlay, as this usually requires a high degree of hardware design expertise. 

There are a number of components to creating an overlay:

* Overlay design
* Transfer of data between PS/PL
* C library/driver
* Python API
* Packaging the overlay

This section will give an overview of the process of creating an overlay and integrating it into PYNQ, but will not cover the hardware design process in detail. Hardware design will be familiar to Zynq, and FPGA hardware developers. 


Overlay design
=======================

An overlay consists of two main parts; the PL design (bitstream) and the project block diagram TCL file. 

PL Design
------------------

The Xilinx® Vivado software is used to create a Zynq design. A *bitstream* or *binary* file (.bit file) will be generated that can be used to program the Zynq PL.

The free WebPack version of Vivado can be used with mid-range Zynq devices (XC7Z007S – XC7Z7030), which includes the PYNQ-Z1 board (XC7Z020).
https://www.xilinx.com/products/design-tools/vivado/vivado-webpack.html

Programmability
^^^^^^^^^^^^^^^^^

An overlay should have post-bitstream programmability to allow customization of the system. A number of reusable PYNQ IP blocks are available to support programmability. For example, an IOP can be used on Pmod, and Arduino interfaces. DIO IP can be reused to provide run-time configurability. 

PYNQ reusable IP is covered in \***

Zynq PS settings
^^^^^^^^^^^^^^^^^^^^^

There are some differences between the standard Zynq design process, and designing overlays for PYNQ. A Vivado project for a Zynq design consists of two parts; the PL design, and the PS configuration settings. The PS configuration includes settings for system clocks, including the clocks used in the PL. 

The PYNQ image which is used to boot the board configures the Zynq PS at boot time. Overlays are downloaded as required by the programmer, and will not reconfigure the Zynq PS. This means that overlay designers should ensure the PS settings in their Vivado project match the PYNQ image settings. 

If any changes are required from the base project settings, for example, if a new overlay needs a different clock setting, the clock must be configured from Python before the new overlay is downloaded. The original setting should be restored before a new overlay is loaded. 


Block Diagram TCL
==================

The block diagram TCL can be used by PYNQ to automatically identify IP, functionality, control and other signals in the overlay. Based on this information, drivers can be automatically assigned, features enabled or disabled, and signals can be connected to corresponding API functions. 

The block diagram TCL file is automatically generated in Vivado by exporting it at the end of the overlay design process. It should be provided in the same location as the bitstream when downloading an overlay. The PYNQ PL class will automatically parse the TCL. 

A custom, or manually created TCL file can be used to build a Vivado project, but this TCL files should not be exported and used when loading an overlay bitstream. Vivado should be used to generate and export the TCL file for the block diagram. This automatically generated TCL should ensure that it can be parsed correctly by the PYNQ PL class. 

Generate overlay TCL file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To generate the TCL for the Block Diagram from the Vivado GUI:

   * Click **File > Export > Block Design**  

Or, run the following in the tcl console:

.. code-block:: console

   write_bd_tcl
      
The tcl filename should match the .bit filename. E.g. my_overlay.bit and my_overlay.tcl

The tcl is parsed when the overlay is instantiated (not when it is downloaded). 

.. code-block:: python

   from pynq import Overlay
   ol = Overlay("base.bit") # tcl is parsed here

   
An error will be displayed if a tcl is not available when attempting to download an overlay, or if the tcl filename does not match the .bit file name.

ip_dict 
-----------------------------------

The PYNQ PL class parses the TCL and generates a dictionary called ip_dict containing the names of IP in a specific overlay, and their address in the system memory map.
 
The dictionary can be used to refer to an IP by name in your Python code, rather than by a hard coded address. It can also check the IP available in an overlay. 

To show the IP dictionary of the overlay, run the following:

.. code-block:: python

   from pynq import Overlay
   OL = Overlay("base.bit")
   OL.ip_dict

Each entry in this IP dictionary that is returned is a key-value pair.
 
E.g.: 

``'SEG_axi_dma_0_Reg': [2151677952, 65536, None],``

Note, this parses the TCL file that was exported with the bitstream. It does not check the overlay currently running in the PL. 

The key of the entry is the IP instance name; all the IP instance names are parsed from the `*.tcl` file (e.g. `base.tcl`) in the address segment section. The value of the entry is a list of 3 items:

   - The first item shows the base address of the addressable IP (as an int).
   - The second item shows the address range in bytes (as an int).
   - The third item records the state associated with the IP. It is `None` by default, but can be user defined.

   
Similarly, the PL package can be used to find the addressable IPs currently in the programmable logic:

.. code-block:: python

   from pynq import PL
   PL.ip_dict


Existing Overlays
=========================

Existing overlays can be used as a starting point to create a new overlay. The *base* overlay can be found in the boards directory in the Pynq repository, and includes reference IP for peripherals on the board: 

   ``<GitHub repository>/boards/<board name>/vivado/base``
  
A makefile exists in each folder that can be used to rebuild the Vivado project and generate the bitstream and TCL for the overlay. 

The bitstream and tcl for the overlay are available on the board, and also in the GitHub project repository: 

   ``<GitHub Repository>/boards/<board name>/bitstream/``

