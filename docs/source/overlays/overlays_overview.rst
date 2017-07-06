Introduction to Overlays
============================
   
Overlay Concept
---------------------

The Xilinx® Zynq® All Programmable device is an SOC based on a dual-core ARM® Cortex®-A9 processor (referred to as the *Processing System* or **PS**), integrated with FPGA fabric (referred to as  *Programmable Logic* or **PL**). The *PS* subsystem includes a number of dedicated peripherals (memory controllers, USB, Uart, IIC, SPI etc) and can be extended with additional hardware IP in a *PL* Overlay. 

.. image:: ../images/zynq_block_diagram.jpg
   :align: center

Overlays, or hardware libraries, are programmable/configurable FPGA designs that extend the user application from the Processing System of the Zynq into the Programmable Logic. Overlays can be used to accelerate a software application, or to customize the hardware platform for a particular application.

For example, image processing is a typical application where the FPGAs can provide acceleration. A software programmer can use an overlay in a similar way to a software library to run some of the image processing functions (e.g. edge detect, thresholding etc.) on the FPGA fabric. 
Overlays can be loaded to the FPGA dynamically, as required, just like a software library. In this example, separate image processing functions could be implemented in different overlays and loaded from Python on demand.

PYNQ provides a Python interface to allow overlays in the *PL* to be controller from Python running in the *PS*. FPGA design is a specialized task which requires hardware engineering knowledge and expertise. PYNQ overlays are created by hardware designers, and wrapped with this PYNQ Python API. Software developers can then use the Python interface to program and control specialized hardware overlays without needing to design an overlay themselves. This is analogous to software libraries created by expert developers which are then used by many other software developers working at the application level. 

Using Overlays
--------------------

New overlays can be loaded as the system is running. The PYNQ *Overlay* class is used to load an overlay. Once the Overlay class is imported, the overlay can be instantiated by specifying the name of the bitstream:

.. code-block:: python

   from pynq import Overlay
   overlay = Overlay("base.bit")

Creating the overlay instance, will also download the bitstream to the Zynq PL
    
Once an overlay has been loaded, a Python API for the overlay can be used to interact with the overlay. 

To discover what is in an overlay, ``help`` can be run on the overlay instance. 

.. code-block:: python

   help(overlay)
   
This will give a listing of the IP and drivers available. 

As an example, where the overlay includes an LED IP, ``help()`` will report the *leds* object exists, and that it is an *AxiGPIO* class:

.. code-block:: console

   leds : AxiGPIO
   4-bit output GPIO for interacting with the green LEDs LD0-3

Running help on the *leds* object will report that it has a ``write()`` function that takes a value and a mask:

.. ode-block:: console

   write(self, val, mask)
       Set the state of the output pins

The LEDs can be turned on and off by writing an appropriate value:

.. code-block:: python

   overlay.leds.write(1, 0xf)
   overlay.leds.write(2, 0xf)
   overlay.leds.write(4, 0xf)
   
Available overlays 
--------------------

There are two overlays that ship with PYNQ, the base overlay, and the DIO - Digital Interfacing Overlay. 

Base overlay
^^^^^^^^^^^^^^

The default PYNQ overlay, is the *base* overlay. It is downloaded to the Zynq PL at boot time, so is available for use immediately after boot. The base overlay is intended to provide basic functionality and connect all peripherals available on the board. The base overlay will be covered in the next section. 

Digital Interfacing Overlay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Digital Interfacing overlay provides digital logic functions controllable from Python. 


The base overlay and DIO will be covered in the next sections. 


Other overlays
^^^^^^^^^^^^^^^^^

Any other overlays can be installed on the board using pip. A selection of third party overlays can be viewed on the www.pynq.io/examples webpage.  

A list of third party overlays can be found in the PYNQ readme. 

Creating an overlay
---------------------

Overlays can be used to build a custom platform, accelerate software applications, or to offload software from the main CPU to for example, lower the total system power. 

Design of custom hardware or accelerators is a specialised task for an FPGA designer. Creating and packaging overlays, and integration of custom hardware into a PYNQ overlay will be covered in later sections, but the design of hardware IP will not be discussed in detail. An FPGA designer can choose their preferred way of developing IP for a PYNQ overlay - HDL, High Level Synthesis, other methods of designing hardware. 



