 
Base Overlay
===================

The base overlay is the default PYNQ overlay loaded to the PL at boot time. The base overlay connects to all the available board peripherals, allowing them to be used from Python out-of-the box. It is also intended that the base overlay can be used as a reference design for creating new custom overlays. 

The project files for the base overlay can be found here:

boards/Pynq-Z1/base

The makefile and .tcl file can be used to rebuild the overlay. The base overlay will include IP from the VIvado library, and custom IP. Any custom IP can be found in directory:

boards/ip 

For more details on rebuilding the overlay, or creating a new overlay, see the Creating Overlays section. 

