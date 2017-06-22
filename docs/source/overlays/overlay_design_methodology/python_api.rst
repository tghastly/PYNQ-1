Creating a Python API
=========================

The Python API is the user interface for the overlay. It exposes the programmable functionality, and allows the overlay to be used. 

Depending on the software functionality required, an API for a PYNQ overlay can be 

* a simple Python wrapper that interfaces directly with the hardware IP blocks in the overlay
* a more substantial Python layer utilising other Python packages
* a Python library that interfaces to a lower level higher performance library (written in C/C++ for example) to control the overlay

Data Transfer 
----------------

Fundamentally, the overlay API for an overlay will control the transfer of data between the Python environment in the PS, and the overlay in the PL. 

A number of Python classes to support data transfer are available. These are the MMIO, Xlnk, DMA and GPIO classes. Each of these classes correspond to an interface type, and are covered in more detail in the next section. They allow transfer of data by reading and writing registers in an overlay, transfer of data from DRAM to the overlay using DMAs, reading and writing simple control data using GPIOs, and allocation of memory to allow the overlay to write data directly to DRAM that can then be accessed from the Python environment. 

These classes are the building blocks for creating a custom Python API for an overlay. This allows a Python wrapper to interface directly with an overlay.


CFFI
----------

In some instances, the performance of Python classes to manage data transfer to an overlay may not be sufficient. A higher performance driver library can be developed in a lower level language (including C/C++) and optimized for an overlay. The driver functions in the library can be called from Python using CFFI (C Foreign Function Interface).


CFFI provides a simple way to interface with C code from Python. The CFFI package is preinstalled in the PYNQ image. It supports an inline ABI (Application Binary Interface) compatibility mode, which allows you to dynamically load and run functions from executable modules, and an API mode, which allows you to build C extension modules. 


The following example taken from http://docs.python-guide.org/en/latest/scenarios/clibs/ shows the ABI inline mode, calling the C function ``strlen()`` in from Python 

C function prototype:

.. code-block:: c

   size_t strlen(const char*);

The C function prototype is passed to ``cdef()``, and can be called using ``clib``.
   
.. code-block:: python

   from cffi import FFI
   ffi = FFI()
   ffi.cdef("size_t strlen(const char*);")
   clib = ffi.dlopen(None)
   length = clib.strlen(b"String to be evaluated.")
   print("{}".format(length))

C functions inside a shared library can be called from Python using the C Foreign Function Interface (CFFI). The shared library can be compiled online using the CFFI from Python, or it can be compiled offline. 

For more information on CFFI and shared libraries refer to:

http://cffi.readthedocs.io/en/latest/overview.html

http://www.tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html
  
   
To see examples in PYNQ on how to use CFFI, refer to the CMA class or the Audio class, both located:

   ``<GitHub Repository>/pynq/drivers``