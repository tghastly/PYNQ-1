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

__author__      = "Yun Rock Qu"
__copyright__   = "Copyright 2016, Xilinx"
__email__       = "pynq_support@xilinx.com"


# Constants
from . import iop_const
from .iop_const import PMODA
from .iop_const import PMODB
from .iop_const import ARDUINO
from .iop_const import PMOD_GROVE_G1
from .iop_const import PMOD_GROVE_G2
from .iop_const import PMOD_GROVE_G3
from .iop_const import PMOD_GROVE_G4
from .iop_const import ARDUINO_GROVE_I2C
from .iop_const import ARDUINO_GROVE_UART
from .iop_const import ARDUINO_GROVE_G1
from .iop_const import ARDUINO_GROVE_G2
from .iop_const import ARDUINO_GROVE_G3
from .iop_const import ARDUINO_GROVE_G4
from .iop_const import ARDUINO_GROVE_G5
from .iop_const import ARDUINO_GROVE_G6
from .iop_const import ARDUINO_GROVE_G7
from .iop_const import ARDUINO_GROVE_A1
from .iop_const import ARDUINO_GROVE_A2
from .iop_const import ARDUINO_GROVE_A3
from .iop_const import ARDUINO_GROVE_A4

# IOP
from .iop import request_iop
from .devmode import DevMode
