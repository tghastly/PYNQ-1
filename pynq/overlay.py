#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import collections
import importlib.util
import os
import re
import mmap
import math
from copy import deepcopy
from datetime import datetime
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from .mmio import MMIO
from .ps import Clocks
from .pl import PL
from .pl import Bitstream
from .pl import _TCL
from .pl import _get_tcl_name
from .pl import PYNQ_PATH
from .interrupt import Interrupt
from .gpio import GPIO


__author__ = "Yun Rock Qu"
__copyright__ = "Copyright 2016, Xilinx"
__email__ = "pynq_support@xilinx.com"


class DefaultOverlay(PL):
    """This class keeps track of a single bitstream's state and contents.

    The overlay class holds the state of the bitstream and enables run-time
    protection of bindlings.

    Our definition of overlay is: "post-bitstream configurable design".
    Hence, this class must expose configurability through content discovery
    and runtime protection.

    The overlay class exposes the IP and hierarchies as attributes in the
    overlay. If no other drivers are available the `DefaultIP` is constructed
    for IP cores at top level and `DefaultHierarchy` for any hierarchies that
    contain addressable IP. Custom drivers can be bound to IP and hierarchies
    by subclassing `DefaultIP` and `DefaultHierarchy`. See the help entries
    for those class for more details.

    This class stores four dictionaries: IP, GPIO, interrupt controller
    and interrupt pin dictionaries.

    Each entry of the IP dictionary is a mapping:
    'name' -> {phys_addr, addr_range, type, config, state}, where
    name (str) is the key of the entry.
    phys_addr (int) is the physical address of the IP.
    addr_range (int) is the address range of the IP.
    type (str) is the type of the IP.
    config (dict) is a dictionary of the configuration parameters.
    state (str) is the state information about the IP.

    Each entry of the GPIO dictionary is a mapping:
    'name' -> {pin, state}, where
    name (str) is the key of the entry.
    pin (int) is the user index of the GPIO, starting from 0.
    state (str) is the state information about the GPIO.

    Each entry in the interrupt controller dictionary is a mapping:
    'name' -> {parent, index}, where
    name (str) is the name of the interrupt controller.
    parent (str) is the name of the parent controller or '' if attached
    directly to the PS7.
    index (int) is the index of the interrupt attached to.

    Each entry in the interrupt pin dictionary is a mapping:
    'name' -> {controller, index}, where
    name (str) is the name of the pin.
    controller (str) is the name of the interrupt controller.
    index (int) is the line index.

    Attributes
    ----------
    bitfile_name : str
        The absolute path of the bitstream.
    bitstream : Bitstream
        The corresponding bitstream object.
    ip_dict : dict
        All the addressable IPs from PS7. Key is the name of the IP; value is
        a dictionary mapping the physical address, address range, IP type,
        configuration dictionary, and the state associated with that IP:
        {str: {'phys_addr' : int, 'addr_range' : int,
               'type' : str, 'config' : dict, 'state' : str}}.
    gpio_dict : dict
        All the GPIO pins controlled by PS7. Key is the name of the GPIO pin;
        value is a dictionary mapping user index (starting from 0),
        and the state associated with that GPIO pin:
        {str: {'index' : int, 'state' : str}}.
    interrupt_controllers : dict
        All AXI interrupt controllers in the system attached to
        a PS7 interrupt line. Key is the name of the controller;
        value is a dictionary mapping parent interrupt controller and the
        line index of this interrupt:
        {str: {'parent': str, 'index' : int}}.
        The PS7 is the root of the hierarchy and is unnamed.
    interrupt_pins : dict
        All pins in the design attached to an interrupt controller.
        Key is the name of the pin; value is a dictionary
        mapping the interrupt controller and the line index used:
        {str: {'controller' : str, 'index' : int}}.

    """
    if CPU_ARCH_IS_SUPPORTED:
        pass
    else:
        warnings.warn("Unsupported CPU Architecture", ResourceWarning)
        
    def __init__(self, bitfile_name):
        """Return a new Overlay object.

        An overlay instantiates a bitstream object as a member initially.

        Note
        ----
        This class requires a Vivado '.tcl' file to be next to bitstream file
        with same name (e.g. base.bit and base.tcl).

        Parameters
        ----------
        bitfile_name : str
            The bitstream name or absolute path as a string.

        """
        super().__init__()

        # Set the bitstream
        self.bitstream = Bitstream(bitfile_name)
        self.bitfile_name = self.bitstream.bitfile_name
        tcl = _TCL(_get_tcl_name(self.bitfile_name))
        self.ip_dict = tcl.ip_dict
        self.gpio_dict = tcl.gpio_dict
        self.interrupt_controllers = tcl.interrupt_controllers
        self.interrupt_pins = tcl.interrupt_pins
        self.clock_dict = tcl.clock_dict

        description = deepcopy(tcl.ip_dict)
        for name, entry in description.items():
            entry['_gpio'] = dict()
            entry['_interrupts'] = dict()

        description['_interrupts'] = self.interrupt_pins
        for k, v in self.interrupt_pins.items():
            (ipname, _, pinname) = k.rpartition('/')
            if ipname in description:
                description[ipname]['_interrupts'][pinname] = v

        gpio_pins = dict()
        for gpio in self.gpio_dict.values():
            for p in gpio['pins']:
                gpio_pins[p] = gpio
                (ipname, _, pinname) = p.rpartition('/')
                if ipname in description:
                    description[ipname]['_gpio'][pinname] = gpio
        description['_gpio'] = gpio_pins
        self.description = description
        self._ip_map = _IPMap("", description)
        self.download()

    def __getattr__(self, key):
        if self.is_loaded():
            return getattr(self._ip_map, key)
        else:
            raise RuntimeError("Overlay not currently loaded")

    def download(self):
        """The method to download a bitstream onto PL.

        Note
        ----
        After the bitstream has been downloaded, the "timestamp" in PL will be
        updated. In addition, all the dictionaries on PL will
        be reset automatically.

        Returns
        -------
        None

        """
        for i in self.clock_dict:
            enable = self.clock_dict[i]['enable']
            div0 = self.clock_dict[i]['divisor0']
            div1 = self.clock_dict[i]['divisor1']
            if enable:
                Clocks.set_fclk(i, div0, div1)
            else:
                Clocks.set_fclk(i)

        self.bitstream.download()
        PL.reset()

    def is_loaded(self):
        """This method checks whether a bitstream is loaded.

        This method returns true if the loaded PL bitstream is same
        as this Overlay's member bitstream.

        Returns
        -------
        bool
            True if bitstream is loaded.

        """
        PL.client_request()
        PL.server_update()
        if not self.bitstream.timestamp == '':
            return self.bitstream.timestamp == PL._timestamp
        else:
            return self.bitfile_name == PL._bitfile_name

    def reset(self):
        """This function resets all the dictionaries kept in the overlay.

        This function should be used with caution.

        Returns
        -------
        None

        """
        tcl = _TCL(_get_tcl_name(self.bitfile_name))
        self.ip_dict = tcl.ip_dict
        self.gpio_dict = tcl.gpio_dict
        self.interrupt_controllers = tcl.interrupt_controllers
        self.interrupt_pins = tcl.interrupt_pins
        if self.is_loaded():
            PL.reset()

    def load_ip_data(self, ip_name, data):
        """This method loads the data to the addressable IP.

        Calls the method in the super class to load the data. This method can
        be used to program the IP. For example, users can use this method to
        load the program to the Microblaze processors on PL.

        Note
        ----
        The data is assumed to be in binary format (.bin). The data name will
        be stored as a state information in the IP dictionary.

        Parameters
        ----------
        ip_name : str
            The name of the addressable IP.
        data : str
            The absolute path of the data to be loaded.

        Returns
        -------
        None

        """
        PL.load_ip_data(ip_name, data)
        self.ip_dict[ip_name]['state'] = data

    def __dir__(self):
        return sorted(set(super().__dir__() +
                          list(self.__dict__.keys()) + 
                          [h for h in self._ip_map._hierarchies] +
                          [i for i in self._ip_map._ipnames]))


_ip_drivers = dict()
_hierarchy_drivers = collections.deque()


class RegisterIP(type):
    """Meta class that binds all registers all subclasses as IP drivers

    The `bindto` attribute of subclasses should be an array of strings
    containing the VLNV of the IP the driver should bind to.

    """
    def __init__(cls, name, bases, attrs):
        if 'bindto' in attrs:
            for vlnv in cls.bindto:
                _ip_drivers[vlnv] = cls
        return super().__init__(name, bases, attrs)


class DefaultIP(metaclass=RegisterIP):
    """Driver for an IP without a more specific driver

    This driver wraps an MMIO device and provides a base class
    for more specific drivers written later. It also provides
    access to GPIO outputs and interrupts inputs via attributes. More specific
    drivers should inherit from `DefaultIP` and include a
    `bindto` entry containing all of the IP that the driver
    should bind to. Subclasses meeting these requirements will
    automatically be registered.

    Attributes
    ----------
    mmio : pynq.MMIO
        Underlying MMIO driver for the device
    _interrupts : dict
        Subset of the PL.interrupt_pins related to this IP
    _gpio : dict
        Subset of the PL.gpio_dict related to this IP

    """

    def __init__(self, description):
        self.mmio = MMIO(description=description)
        self._iterrupts = description['_interrupts']
        self._gpio = description['_gpio']
        for interrupt in self._interrupts.keys():
            setattr(self, interrupt, Interrupt(interrupt))
        for gpio, entry in self._gpio.items():
            gpio_number = pynq.GPIO.get_gpio_pin(entry['index'])
            setattr(self, gpio, GPIO(gpio_number, 'out'))

    def read(self, offset=0):
        """Read from the MMIO device

        Parameters
        ----------
        offset : int
            Address to read

        """
        return self.mmio.read(offset)

    def write(self, offset, value):
        """Write to the MMIO device

        Parameters
        offset : int
            Address to write to
        value : int or bytes
            Data to write

        """
        self.mmio.write(offset, value)


def _create_ip(desc):
    if desc['type'] in _ip_drivers:
        return _ip_drivers[desc['type']](description=desc)
    else:
        return DefaultIP(description=desc)


def _partitiondict(dictionary, key):
    return {k.partition('/')[2]: v
            for k, v in dictionary.items()
            if k.startswith('{}/'.format(key))}


def _gethierarchydriver(fullpath, desc):
    for hip in _hierarchy_drivers:
        if hip.checkhierarchy(fullpath, desc):
            return hip
    return DocumentHierarchy


def _getipdriver(desc):
    if desc['type'] in _ip_drivers:
        return _ip_drivers[desc['type']]
    else:
        return DefaultIP


class _IPMap:

    def __init__(self, path, desc):
        hierarchies = {k.partition('/')[0]
                       for k in desc.keys() if k.count('/')}
        ipnames = {k for k, v in desc.items() if k.count('/') ==
                   0 and 'type' in v}

        self._interrupts = {k for k in desc['_interrupts'].keys()
                            if k.count('/') == 0}
        self._gpio = {k for k in desc['_gpio'].keys() if k.count('/') == 0}
        self._description = desc
        self._path = path
        self._hierarchies = {}
        for h in hierarchies:
            if self._path:
                fullpath = "{}/{h}".format(self._path)
            else:
                fullpath = h
            driver = _gethierarchydriver(fullpath,
                                         self.hierarchydescription(h))
            self._hierarchies[h] = driver
        self._ipdrivers = {k: _getipdriver(desc[k]) for k in ipnames}

    def hierarchydescription(self, hierarchy):
        subdesc = _partitiondict(self._description, hierarchy)
        subdesc['_interrupts'] = _partitiondict(
            self._description['_interrupts'], hierarchy)
        subdesc['_gpio'] = _partitiondict(
            self._description['_gpio'], hierarchy)

        return subdesc

    def __getattr__(self, key):
        print('__getattr__({})'.format(key))
        if self._path:
            fullpath = "{self._path}/{}".format(key)
        else:
            fullpath = key
        if key in self._hierarchies:
            subdesc = self.hierarchydescription(key)
            hierarchy = self._hierarchies[key](fullpath, subdesc)
            setattr(self, key, hierarchy)
            return hierarchy
        elif key in self._ipdrivers:
            ip_description = self._description[key]
            if 'fullpath' not in ip_description:
                ip_description['fullpath'] = fullpath
            driver = self._ipdrivers[key](ip_description)
            setattr(self, key, driver)
            return driver
        elif key in self._interrupts:
            interrupt = Interrupt(key)
            setattr(self, key, interrupt)
            return interrupt
        elif key in self._gpio:
            gpio_number = pynq.GPIO.get_gpio_pin(self._gpio[key]['index'])
            gpio = GPIO(gpio_number, 'out')
            setattr(self, key, gpio)
            return gpio
        else:
            raise AttributeError(
                "Could not find IP or hierarchy {} in overlay".format(key))

    def __dir__(self):
        return sorted(set(super().__dir__() +
                          list(self.__dict__.keys()) +
                          [h for h in self._hierarchies] +
                          [i for i in self._ipnames] +
                          [i for i in self._interrupts] +
                          [g for g in self._gpio]))


def _classname(class_):
    return "{}.{}".format(class_.__module__,class_.__name__)


def _builddocstring(ipmap, name, type_):
    lines = []
    lines.append("Default documentation for {} {}. The following".format(type_, name))
    lines.append("attributes are available on this {type_}:".format(type_))
    lines.append("")

    lines.append("IP Blocks")
    lines.append("----------")
    if ipmap._ipdrivers:
        for ip, driver in ipmap._ipdrivers.items():
            lines.append("{:<20} : {}".format(ip, _classname(driver)))
    else:
        lines.append("None")
    lines.append("")

    lines.append("Hierarchies")
    lines.append("-----------")
    if ipmap._hierarchies:
        for hierarchy, driver in ipmap._hierarchies.items():
            lines.append("{:<20} : {}".format(hierarchy , _classname(driver)))
    else:
        lines.append("None")
    lines.append("")

    lines.append("Interrupts")
    lines.append("----------")
    if ipmap._interrupts:
        for interrupt in ipmap._interrupts:
            lines.append("{:<20} : pynq.interrupt.Interrupt".format(interrupt ))
    else:
        lines.append("None")
    lines.append("")

    lines.append("GPIO Outputs")
    lines.append("------------")
    if ipmap._gpio:
        for gpio in ipmap._gpio:
            lines.append("{:<20} : pynq.gpio.GPIO".format(gpio))
    else:
        lines.append("None")
    lines.append("")
    return '\n    '.join(lines)


def DocumentOverlay(bitfile):
    class DocumentedOverlay(DefaultOverlay):
        def __init__(self):
            super().__init__(bitfile)
    overlay = DocumentedOverlay()
    DocumentedOverlay.__doc__ = builddocstring(overlay._ip_map,
                                               bitfile,
                                               "overlay")
    return overlay


def DocumentHierarchy(fullpath, description):
    class DocumentedHierarchy(DefaultHierarchy):
        def __init__(self):
            super().__init__(fullpath, description)
    hierarchy = DocumentedHierarchy()
    DocumentedHierarchy.__doc__ = builddocstring(hierarchy,
                                                 fullpath,
                                                 "hierarchy")
    return hierarchy


class RegisterHierarchy(type):
    """Metaclass to register classes as hierarchy drivers

    Any class with this metaclass an the `checkhierarchy` function
    will be registered in the global driver database

    """
    def __init__(cls, name, bases, attrs):
        if 'checkhierarchy' in attrs:
            _hierarchy_drivers.appendleft(cls)
        return super().__init__(name, bases, attrs)


class DefaultHierarchy(_IPMap, metaclass=RegisterHierarchy):
    """Hierarchy exposing all IP and hierarchies as attributes

    This Hierarchy is instantiated if no more specific hierarchy class
    registered with register_hierarchy_driver is specified. More specific
    drivers should inherit from `DefaultHierarachy` and call it's constructor
    in __init__ prior to any other initialisation. `checkhierarchy` should
    also be redefined to return True if the driver matches a hierarchy.
    Any derived class that meets these requirements will automatically be
    registered in the driver database.

    """

    def __init__(self, path, description=None):
        if description is None:
            ip_dict = PL.ip_dict
            filtered_dict = {k.replace('{}/'.format(path), '', 1): v
                             for k, v in ip_dict.items()
                             if k.startswith('{}/'.format(path))}
            description = filtered_dict
        self.description = description
        super().__init__(path, description)

    @staticmethod
    def checkhierarchy(path, description):
        """Function to check if the driver matches a particular hierarchy

        This function should be redefined in derived classes to return True
        if the description matches what is expected by the driver. The default
        implementation always returns False so that drivers that forget don't
        get loaded for hierarchies they don't expect.

        """
        return False


def Overlay(bitfile, class_=None):
    bitfile_path = os.path.join(
        PYNQ_PATH, bitfile.replace('.bit', ''), bitfile)
    python_path = os.path.splitext(bitfile_path)[0] + '.py'
    if class_:
        return class_(bitfile)
    elif os.path.exists(python_path):
        spec = importlib.util.spec_from_file_location(
            os.path.splitext(os.path.basename(bitfile_path))[0],
            python_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Overlay(bitfile)
    else:
        return DocumentOverlay(bitfile)
