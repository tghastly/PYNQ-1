
Video Subsystem
============================

The Video subsystem consists of a HDMI-in block, a HDMI-out block, and a Video DMA.  
   
.. image:: ../../images/video_subsystem.png
   :align: center
   
Video data can be captured from the HDMI-in, and streammed to DRAM, or directly to the HDMI-out by the VDMA. Data can also be streamed from DRAM to the HDMI-out. 

The video subsystem also supports simplle color space conversions from YCrCb to RGB and back. This is acomplished by hardware blocks integrated into both the HDMI-in and HDMI-out blocks. 

HDMI-In
------------
   
.. image:: ../../images/hdmi_in_subsystem.png
   :align: center

The Pixel Unpack and the Color Convert block allow conversion between different color spaces at runtime. Supported color spaces include: RGB (24-bit), RGBA (32-bit), BGR (24-bit), YCbCr (24-bit), and grayscale (8-bit).


HDMI-Out
--------------
   
.. image:: ../../images/hdmi_out_subsystem.png
   :align: center

The HDMI-out is similar to HDMI-in. It has a Pixel Pack block (instead of the *Unpack* block for HDMI-in) and a Color Convert block. 


Examples
------------------

Basic HDMI operation
^^^^^^^^^^^^^^^^^^^^^^^^

Set up an instnace of the HDMI-in, and HDMI-out. 

.. code-block:: Python

    from pynq.lib.video import HDMIIn, HDMIOut

    hdmi_in = HDMIIn('video')
    hdmi_out = HDMIOut('video')

The HDMI-in does not need to be configured. It will assume the defualt configuration. The HDMI-in mode can be used to configure the HDMI-out. This specifies the color space. 

.. code-block:: Python

    hdmi_out.configure(hdmi_in.mode)

Both HDMI controllers can then be started

.. code-block:: Python

    hdmi_in.start()
    hdmi_out.start()

To do a simple stream from HDMI-in to HDMI-out, the two streams can be tied together. This takes the unmodified input stream and passes it directly to the output. 

.. code-block:: Python

    hdmi_in.tie(hdmi_out)


Individual frames can also be read and written. 

.. code-block:: Python

    frame = hdmi_in.readframe()
    hdmi_out.writeframe(frame)
    
This woul allow some processing could be carried out on the HDMI-in frame before writing it to the HDMI-out.


.. code-block:: Python

    frame = hdmi_in.readframe()
    hdmi_out.writeframe(frame)


For more examples, see the Video notebooks. 