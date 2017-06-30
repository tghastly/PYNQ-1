**********************
Attributes
**********************

Each overlay has a set of attributes associated with it. Attributes include a list of IP and versions that exist inside the overlay, a list of interrupt signals connected to IP, and a list of GPIO in the design. 

Overlay attributes allow discovery of available IP in an overlay in a consistent maner, and allow a simple way to bind an API to an IP, and to ease reuse of IP between overlays. 


from pynq import Overlay

overlay = Overlay('base.bit')
help(overlay)
The attribute overlay has three main design goals
Allow overlay users to find out what is inside and overlay in a consistent manner
Provide a simple way for developers of new hardware designs to test new IP
Facilitate reuse of IP between Overlays