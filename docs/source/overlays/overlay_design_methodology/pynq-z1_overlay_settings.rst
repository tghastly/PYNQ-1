******************************
PYNQ-Z1 board settings
******************************

For information on the board, see the Digilent PYNQ-Z1 resource site:
https://reference.digilentinc.com/reference/programmable-logic/pynq-z1/start

Base overlay project
=======================

The source files for the *base* overlay can be found in the PYNQ GitHub. The project can be rebuilt using the makefile/TCL available here:

.. code-block:: console:

   ``<GitHub repository>/boards/<board name>/vivado/base``


Vivado board files
=========================

Vivado board files can be used to create a new project for the PYNQ-Z1:

Download the `PYNQ-Z1 board files <https://github.com/cathalmccabe/pynq-z1_board_files/raw/master/pynq-z1.zip>`_

To install the board files, extract, and copy the board files folder to:

.. code-block:: console:

   <Xilinx installation directory>\Vivado\<version>\data\boards

If Vivado is open, it must be restart to load in the new project files. 


Pynq-Z1 XDC constraints file
=============================

The PYNQ-Z1 Master XDC (I/O constraints):
https://reference.digilentinc.com/_media/reference/programmable-logic/pynq-z1/pynq-z1_c.zip



