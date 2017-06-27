Base Overlay overview
======================

The *base* overlay is the default overlay. It is included in the SD card image, and is loaded to the Zynq PL at boot time. The base overlay design includes the hardware IP to control the board peripherals, and connects these IP blocks to the Zynq PS.

Board peripherals typically include GPIO devices (LEDs, Switches, Buttons), Video, Audio, and any other custom interfaces including Pmods and Arduino headers. In the case of header port, the base overlay may include an IOP for the interface, or a simple GPIO interface.

Once the system boots, all board peripherals should be available to use via the base overlay. 

The base overlay design can also be used as a reference design for creating new overlays. The base overlay project will include the setting which should be used for any new overlay design. 

Any controllers, or IP that are not required can be removed from the base overlay design, and any custom hardware blocks can be added. 

Base overlay project files
----------------------------

All project source files for the base overlay can be found here:

    ``<GitHub Repository>/boards/<board>/base``

The makefile and .tcl file in the directory can be used to rebuild the overlay. 

The base overlay can include IP from the Vivado library, and custom IP. Any custom IP for overlays can be found in here:

    ``<GitHub Repository>/boards/ip`` 

For more details on rebuilding the overlay, or creating a new overlay, see the Creating Overlays section. 


